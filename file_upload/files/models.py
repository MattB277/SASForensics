from django.db import models
from .utils import upload_to_based_on_type



# Create your models here.
from django.db import models

class Case(models.Model):
    case_id=models.CharField(max_length=50, primary_key=True, unique=True)
    case_number=models.CharField(max_length=20, unique=True)
    type_of_crime=models.CharField(max_length=255)
    date_opened = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[("New Evidence","New Evidence"), ("Updated Information","Updated Information"), ("No changes", "No changes")])
    
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
    