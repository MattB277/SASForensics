from django.test import TestCase
from case_api.models import Case
from case_api.serializers import CaseSerializer
from django.contrib.auth.models import User

class CaseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.case = Case.objects.create(case_number="123456", created_by=self.user)

    def test_case_serializer(self):
        serializer = CaseSerializer(self.case)
        self.assertEqual(serializer.data["case_number"], "123456")
