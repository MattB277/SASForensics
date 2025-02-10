from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import upload_to_based_on_type
from django.utils.text import slugify
import os

class Document(models.Model):
    file = models.FileField(upload_to='case_api/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Case(models.Model):
    case_id = models.AutoField(primary_key=True, unique=True)
    case_number = models.CharField(max_length=20, unique=True)
    crime_type = models.CharField(max_length=255)
    date_opened = models.DateTimeField()
    last_updated = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="created_cases")
    assigned_users = models.ManyToManyField(User, related_name="assigned_cases", blank=True)
    reviewers = models.ManyToManyField(User, related_name="case_reviewers", blank=True)
    related_cases = models.ManyToManyField("self", related_name="referenced_cases", blank=True, symmetrical=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new_evidence', 'New Evidence'),
            ('new_collaboration', 'New Collaboration'),
            ('no_changes', 'No Changes'),
        ],
        default='no_changes',
    ) 
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_opened = timezone.now()
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

class UserCaseAccessRecord(models.Model):
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case_access_records", null=False, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="case_access_records", null=False, blank=False)
    last_accessed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("New Evidence","New Evidence"), ("Updated Information","Updated Information"), ("No changes", "No changes")])


def upload_to_based_on_type(instance, filename):
    extension = filename.split('.')[-1]
    if extension.lower() in ['pdf', 'jpeg', 'docx', 'mp4']:
        folder = 'pdfs/' if extension.lower() == 'pdf' else 'images/'
    else:
        folder = 'others/'
    return f"{folder}{filename}"

class File(models.Model):
    file_id = models.AutoField(primary_key=True, unique=True)
    ALLOWED_FILE_TYPES = ['pdf', 'mp4', 'jpeg', 'docx']
    file = models.FileField(upload_to=upload_to_based_on_type)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    case_id = models.ForeignKey(
        "Case",
        on_delete=models.SET_NULL,
        related_name="files",
        null=True,
        blank=True,
    )
    file_type = models.CharField(
        max_length=20,
        choices=[("pdf", "pdf"), ("mp4", "mp4"), ("jpeg", "jpeg"), ("docx", "docx")],
        blank=True,
    )

    def __str__(self):
        return self.file.name
    
    def display_name(self):
        return self.file.name.split("/")[-1]

    def file_extension(self):
        return self.file.name.split('.')[-1].lower()

    def save(self, *args, **kwargs):
        if not self.file_type:
            self.file_type = self.file_extension()
        super().save(*args, **kwargs)

class CaseChangelog(models.Model):
    change_id = models.AutoField(primary_key=True, blank=False)
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case_changelog_record")
    change_date = models.DateTimeField(auto_now=True)
    change_details = models.CharField(max_length=70, blank=False)
    change_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    type_of_change = models.CharField(max_length=50, choices=[("Added Evidence","Added Evidence"), ("Updated Information","Updated Information"), ("Assigned Detective", "Assigned Detective"), ("Assigned Reviewer", "Assigned Reviewer"), ("Created Connection","Created Connection"), ("Created Case", "Created Case")])

class DocChangelog(models.Model):
    change_id = models.AutoField(primary_key=True, blank=False)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE, related_name="file_changelog_record")
    change_date = models.DateTimeField(auto_now=True)
    change_details = models.CharField(max_length=70, blank=False)
    change_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

class AnalysedDocs(models.Model):
    Analysis_id = models.AutoField(primary_key=True, blank=False)
    file_id = models.OneToOneField(File, on_delete=models.CASCADE, related_name="analysed_document")
    JSON_file = models.FilePathField(blank=False)
    case_number = models.CharField(max_length=20, blank=True)
    reviewed = models.BooleanField(default=False)

class View(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
