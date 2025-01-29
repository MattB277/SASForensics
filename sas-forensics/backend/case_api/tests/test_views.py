from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from case_api.models import Case

class CaseViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")
        self.case = Case.objects.create(case_number="123456", created_by=self.user)

    def test_assign_user(self):
        response = self.client.post(f"/api/cases/{self.case.case_id}/assign-user/", {"user_id": self.user.id})
        self.assertEqual(response.status_code, 200)
