from rest_framework import serializers
from .models import  Case, File, CaseChangelog, DocChangelog, UserCaseAccessRecord
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class FileSerializer(serializers.ModelSerializer):
    # send the analysis url if it exists 
    analysis_json_url = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ['file_id', 'file', 'uploaded_at', 'file_type', 'case_id']

    def get_analysis_json_url(self, instance):
        request = self.context.get('request')
        if hasattr(instance, 'analysed_document') and instance.analysed_document.JSON_file: # if attribute exists, analysis has been created
            url = instance.analysed_document.JSON_file.url
            return request.build_absolute_uri(url) if request else url
        return None # null if analysis does not exist
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['file'] = request.build_absolute_uri(instance.file.url)
        else:
            data['file'] = f"{settings.MEDIA_URL}{instance.file.name}"
        return data

class CaseSerializer(serializers.ModelSerializer):
    assigned_users = serializers.StringRelatedField(many=True)
    reviewers = serializers.StringRelatedField(many=True)
    related_cases = serializers.StringRelatedField(many=True)
    class Meta:
        model = Case
        fields = [
            'case_id', 'case_number', 'crime_type', 'date_opened', 'last_updated',
            'location', 'created_by', 'assigned_users', 'reviewers', 'related_cases','status'
        ]


class CaseChangelogSerializer(serializers.ModelSerializer):
    case_id = serializers.CharField(source='case_id.case_number', read_only=True)
    change_author = serializers.StringRelatedField()

    class Meta:
        model = CaseChangelog
        fields = ['change_id', 'case_id', 'change_date', 'change_details', 'change_author', 'type_of_change']


class DocChangelogSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(source='file_id.file', read_only=True)
    change_author = serializers.StringRelatedField()

    class Meta:
        model = DocChangelog
        fields = ['change_id', 'file_id', 'change_date', 'change_details', 'change_author', 'type_of_change']


class UserCaseAccessRecordSerializer(serializers.ModelSerializer):
    case_id = serializers.StringRelatedField() 
    user_id = serializers.StringRelatedField()

    class Meta:
        model = UserCaseAccessRecord
        fields = ['case_id', 'user_id', 'last_accessed', 'status']

class CaseDetailSerializer(serializers.ModelSerializer):
    assigned_users = serializers.StringRelatedField(many=True)
    reviewers = serializers.StringRelatedField(many=True)
    related_cases = serializers.StringRelatedField(many=True)
    files = FileSerializer(many=True, read_only=True)
    changelog = CaseChangelogSerializer(many=True, read_only=True, source="case_changelog_record")
    access_records = UserCaseAccessRecordSerializer(many=True, read_only=True, source="case_access_records")

    class Meta:
        model = Case
        fields = [
            'case_id', 'case_number', 'type_of_crime', 'date_opened', 'last_updated',
            'location', 'created_by', 'assigned_users', 'reviewers', 'related_cases',
            'files', 'changelog', 'access_records'
        ]

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer