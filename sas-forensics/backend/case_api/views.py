from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Case, File, CaseChangelog, DocChangelog, UserCaseAccessRecord, AnalysedDocs
from .serializers import (
    CaseSerializer, FileSerializer, CaseChangelogSerializer,
    DocChangelogSerializer, UserCaseAccessRecordSerializer, UserSerializer
)
from django.contrib.auth.models import User
import json

class ReactAppView(TemplateView):
    template_name = "react/build/index.html"


class CaseChangeLogView(APIView):
    def get(self, request, case_id, *args, **kwargs):
        changes = CaseChangelog.objects.filter(case_id=case_id).order_by('-change_date')
        if not changes.exists():
            return Response({"error": "No changes found for this case."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CaseChangelogSerializer(changes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatedCasesView(APIView):
    def get(self, request, *args, **kwargs):
        changes_by_type = {
            "evidence": CaseChangelog.objects.filter(type_of_change="Added Evidence"),
            "comments": CaseChangelog.objects.filter(type_of_change="Updated Information"),
            "connections": CaseChangelog.objects.filter(type_of_change="Created Connection"),
        }

        formatted_data = {
            change_type: [
                {
                    "change_details": change.change_details,
                    "added_by": change.change_author.username if change.change_author else "Unknown",
                    "case_id": change.case_id.case_id if change.case_id else None,
                    "change_date": change.change_date.date(),
                }
                for change in changes
            ]
            for change_type, changes in changes_by_type.items()
        }

        return Response(formatted_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def documents_to_review(request):
    """Get document with analysis assigned to reviewer"""
    user = request.user

    cases = Case.objects.filter(reviewers__in=[user])

    files = File.objects.filter(case_id__in=cases).order_by("case_id", "uploaded_at")

    document_list = [
        {
            "file_id": file.file_id,
            "file_name": file.display_name,
            "case_id": file.case_id.case_number if file.case_id else "Unknown",
            "uploaded_at": file.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
        } for file in files]
    
    return Response(document_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_files(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def upload_file(request):
    case_id = request.data.get('case_id')
    if not case_id:
        return Response({"error": "case_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        case = Case.objects.get(case_id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(case_id=case)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_analysis(request, pk):
    """Gets JSON analysis file and file URL for a given file object."""
    file_obj = get_object_or_404(File, pk=pk)

    try:
        analysed_doc = file_obj.analysed_document # access analysed document through reference name set in AnalysedDocs
        with open(analysed_doc.JSON_file, 'r') as f:
            json_data = json.load(f)
        
        return Response({
            "file_url" : request.build_absolute_uri(file_obj.file.url),     # uri for original file
            "json_data": json_data,                                         # read JSON data
            "reviewed": analysed_doc.reviewed                               # reviewed flag
        })
    except AnalysedDocs.DoesNotExist:
        return Response({"error": "Analysis not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_analysis(request, pk):
    """Update JSON analysis if there are changes, and mark it as reviewed."""
    file_obj = get_object_or_404(File, pk = pk)
    try:
        analysed_doc = file_obj.analysed_document
        json_data = request.data.get('json_data', None)
        reviewed = request.data.get('reviewed', None)

        # save updated JSON if provided
        if json_data is not None:
            with open(analysed_doc.JSON_file, 'w') as f:
                json.dump(json_data, f, indent=4)

        # mark analysis as reviewed
        if reviewed is not None:    # only update if react component passes reviewed flag in request
            analysed_doc.reviewed = reviewed
            analysed_doc.save()

        return Response({"message": "Analysis updated Successfully"})
    except AnalysedDocs.DoesNotExist:
        return Response({"error": "Analysis not found"}, status=status.HTTP_404_NOT_FOUND)


def serve_file(request, pk):
    file_obj = get_object_or_404(File, pk=pk)
    response = FileResponse(open(file_obj.file.path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'inline; filename="{file_obj.file.name.split("/")[-1]}"'
    return response


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-last_updated')
    serializer_class = CaseSerializer

    @action(detail=True, methods=['post'], url_path='assign-user')
    def assign_user(self, request, pk=None):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            case = self.get_object()
            user = User.objects.get(id=user_id)
            case.assigned_users.add(user)
            return Response(
                {"success": f"User {user.username} assigned to case {case.case_number}."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='remove-user')
    def remove_user(self, request, pk=None):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            case = self.get_object()
            user = User.objects.get(id=user_id)
            case.assigned_users.remove(user)
            return Response(
                {"success": f"User {user.username} removed from case {case.case_number}."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='users')
    def get_assigned_users(self, request, pk=None):
        case = self.get_object()
        users = case.assigned_users.all()
        return Response(
            [{"id": user.id, "username": user.username} for user in users],
            status=status.HTTP_200_OK,
        )


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=False, methods=['get'], url_path='case/(?P<case_id>[^/.]+)')
    def list_by_case(self, request, case_id=None):
        files = File.objects.filter(case_id=case_id)
        if not files.exists():
            return Response({"detail": "No files found for this case."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CaseChangelogViewSet(viewsets.ModelViewSet):
    queryset = CaseChangelog.objects.all()
    serializer_class = CaseChangelogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type_of_change']


class DocChangelogViewSet(viewsets.ModelViewSet):
    queryset = DocChangelog.objects.all()
    serializer_class = DocChangelogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['change_details']


class UserCaseAccessRecordViewSet(viewsets.ModelViewSet):
    queryset = UserCaseAccessRecord.objects.all()
    serializer_class = UserCaseAccessRecordSerializer


class CaseListCreateView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseListView(ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
