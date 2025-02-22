from django.test import TestCase
from case_api.models import Case
from django.contrib.auth.models import User

class CaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_case_creation(self):
        case = Case.objects.create(case_number="123456", crime_type="Theft", created_by=self.user)
        self.assertEqual(case.case_number, "123456")
