from django.test import TestCase
from case_api.forms import DocumentForm
from django.core.files.uploadedfile import SimpleUploadedFile

class DocumentFormTest(TestCase):
    def test_valid_file_upload(self):
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        form = DocumentForm(data={}, files={"file": file})
        self.assertTrue(form.is_valid())
