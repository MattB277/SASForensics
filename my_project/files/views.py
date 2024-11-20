from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
from .forms import FileForm
from .models import File
from django.http import HttpResponseRedirect
from rest_framework import status


class FileListView(APIView):
    def get(self, request):
        files = File.objects.all()  # Get all uploaded files
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = FileForm()
    return render(request, 'upload_file.html', {'form': form})

def upload_success(request):
    file = File.objects.all()
    return render(request, 'upload_success.html', {'documents': file})

def react_app(request):
    return HttpResponseRedirect("http://localhost:3000/")