from django.contrib import admin
from .models import Document, Case, File, CaseChangelog, DocChangelog, UserCaseAccessRecord

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'case_number', 'crime_type', 'created_by', 'last_updated')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_id', 'file', 'uploaded_at', 'case_id', 'file_type')

@admin.register(CaseChangelog)
class CaseChangelogAdmin(admin.ModelAdmin):
    list_display = ('change_id', 'case_id', 'change_date', 'type_of_change')

@admin.register(DocChangelog)
class DocChangelogAdmin(admin.ModelAdmin):
    list_display = ('change_id', 'file_id', 'change_date', 'change_details')

@admin.register(UserCaseAccessRecord)
class UserCaseAccessRecordAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'user_id', 'last_accessed', 'status')
