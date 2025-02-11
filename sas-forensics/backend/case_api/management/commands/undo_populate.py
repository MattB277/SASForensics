from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from case_api.models import Case, File, CaseChangelog
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Delete users
        user_count = User.objects.filter(username__startswith="officer").delete()[0]
        print(f"Deleted {user_count} users.")

        # Log and delete cases
        cases = Case.objects.filter(case_number__startswith="CASE-")
        print(f"Cases to delete: {cases}")
        case_count = cases.delete()[0]
        print(f"Deleted {case_count} cases.")

        # Log and delete files
        files = File.objects.all()
        print(f"Files to delete: {files}")
        file_count = files.delete()[0]
        print(f"Deleted {file_count} files.")

        # Log and delete changelogs
        changelogs = CaseChangelog.objects.all()
        print(f"Changelogs to delete: {changelogs}")
        changelog_count = changelogs.delete()[0]
        print(f"Deleted {changelog_count} case changelogs.")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'case_api_case';")
