from django.db import models
from .utils import upload_to_based_on_type

# Create your models here.

class Document(models.Model):
    ALLOWED_FILE_TYPES = ['pdf', 'mp4', 'jpeg', 'docx']
    file = models.FileField(upload_to=upload_to_based_on_type)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def file_extension(self):
        return self.file.name.split('.')[-1].lower()