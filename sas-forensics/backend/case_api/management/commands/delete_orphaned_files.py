# upload/management/commands/delete_orphaned_files.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from case_api.models import Document  # Ensure the import matches your app name and model

class Command(BaseCommand):
    help = 'Remove file references from the database if the files are not present locally'

    def handle(self, *args, **kwargs):
        # Get all the file paths stored in the database
        all_files = Document.objects.values_list('file', flat=True)
        
        # Path to the media folder
        media_path = os.path.join(settings.MEDIA_ROOT)

        # Iterate over the files to check if they exist locally
        for file_path in all_files:
            # Check if the file exists locally (relative to MEDIA_ROOT)
            local_file_path = os.path.join(media_path, file_path)
            
            if not os.path.exists(local_file_path):  # If file doesn't exist locally
                # Remove the reference from the database
                Document.objects.filter(file=file_path).delete()
                self.stdout.write(self.style.SUCCESS(f'Removed orphaned file reference: {file_path}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'File exists: {file_path}'))

        self.stdout.write(self.style.SUCCESS('Orphaned file references removal complete.'))
