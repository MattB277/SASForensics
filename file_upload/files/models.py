from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone, timesince
from .utils import upload_to_based_on_type
# Create your models here.
from django.db import models


class Case(models.Model):
    case_id=models.CharField(max_length=50, primary_key=True, unique=True)
    case_number=models.CharField(max_length=20, unique=True)
    type_of_crime=models.CharField(max_length=255)
    date_opened = models.DateTimeField()
    last_updated = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="created_cases")
    assigned_users = models.ManyToManyField(User, related_name="assigned_cases", blank=True)
    reviewers = models.ManyToManyField(User, related_name="case_reviewers", blank=True)
    referenced_cases = models.ManyToManyField(Case, related_name="referenced_cases", blank=True) 
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_opened = timezone.now()

# model to track user accesses per user for every case, should remain a lightweight model!
class UserCaseAccessRecord(models.Model):
    case_id=models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case_access_records", null=False, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="case_access_records", null=False, blank=False)
    last_accessed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("New Evidence","New Evidence"), ("Updated Information","Updated Information"), ("No changes", "No changes")])

class File(models.Model):
    file_id = models.IntegerField(max_length=30, primary_key=True, unique=True) # used for referencing analysed_docs model
    ALLOWED_FILE_TYPES = ['pdf', 'mp4', 'jpeg', 'docx']
    file = models.FileField(upload_to=upload_to_based_on_type)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="files", null=True, blank=True) # updated upon document analysis completion
    file_type = models.CharField(max_length=20, choices=[("pdf","pdf"),("mp4","mp4"),("jpeg","jpeg"),("docx","docx")], blank=True)
    changelog_id = models.ForeignKey(DocChangelog)
    
    def __str__(self):
        return self.file.name

    def file_extension(self):
        return self.file.name.split('.')[-1].lower()
    
    def runAnalysis(self):
        #open file and call JSONAnalysis function from utils.py, use it to update related records/create new analysis output instance in repective model
        pass

    # overriding File save() method to set file_type automatically:
    def save(self, *args, **kwargs):
        if not self.file_type:
            self.file_type = self.file_extension()
        super().save(*args, **kwargs)


class DocChangelog(models.Model):
    file_id = models.OneToOneField(File, on_delete=models.CASCADE) # only delete changes when the document is deleted
    change_id = models.IntegerField(max_length=30, primary_key=True, blank=False)
    change_date = models.DateTimeField(auto_now=True)
    change_details = models.CharField(max_length=70, blank=False)
    change_author = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True) # if a user instance is deleted, keep record of the changes they made! (allow null entry)

class View(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title   
    