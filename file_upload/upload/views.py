from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = DocumentForm()
    return render(request, 'upload_file.html', {'form': form})

def upload_success(request):
    documents = Document.objects.all()
    return render(request, 'upload_success.html', {'documents': documents})