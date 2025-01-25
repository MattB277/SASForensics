from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data['file']
        allowed_file_types = ['pdf', 'mp4', 'jpeg', 'jpg', 'docx']
        extension = file.name.split('.')[-1].lower()
        if extension not in allowed_file_types:
            raise forms.ValidationError('Unsupported file type.')
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size exceeds 10MB.')
        return file
