from django.db import models
from .utils import upload_to_based_on_type



# Create your models here.
from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name
    
class File(models.Model):
    ALLOWED_FILE_TYPES = ['pdf', 'mp4', 'jpeg', 'docx']
    file = models.FileField(upload_to=upload_to_based_on_type)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def file_extension(self):
        return self.file.name.split('.')[-1].lower()
    
class View(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title   
    