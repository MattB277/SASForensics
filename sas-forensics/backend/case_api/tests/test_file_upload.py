from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from case_api.models import Case, File


class FileUploadTest(TestCase):
    def setUp(self):
        """Initialize test data"""
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")
        self.case = Case.objects.create(
            case_number="123456", crime_type="Theft", created_by=self.user
        )

        # Create a test file
        self.valid_file = SimpleUploadedFile(
            "test.pdf", b"file_content", content_type="application/pdf"
        )
        self.invalid_file = SimpleUploadedFile(
            "test.exe", b"malware", content_type="application/x-msdownload"
        )

    def test_get_file_list(self):
        """Test to get the file list"""
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_valid_file(self):
        """Test upload of valid files"""
        data = {"file": self.valid_file, "case_id": self.case.case_id}
        response = self.client.post("/api/files/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)

    def test_upload_invalid_file(self):
        """Test upload invalid file format"""
        data = {"file": self.invalid_file, "case_id": self.case.case_id}
        response = self.client.post("/api/files/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_file_by_case(self):
        """Test to get files by case"""
        file_instance = File.objects.create(file="pdfs/test.pdf", case_id=self.case)
        response = self.client.get(f"/api/cases/{self.case.case_id}/files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_file(self):
        """Test to get a single file"""
        file_instance = File.objects.create(file="pdfs/test.pdf", case_id=self.case)
        response = self.client.get(f"/api/files/{file_instance.file_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
