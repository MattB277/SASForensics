from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from case_api.models import Case

class CaseViewSetTest(TestCase):
    def setUp(self):
        """Initialize test data"""
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")
        self.case = Case.objects.create(
            case_number="123456", crime_type="Theft", created_by=self.user
        )

    def test_get_case_list(self):
        """Test to get case list"""
        response = self.client.get("/api/cases/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_case_detail(self):
        """Test to get details of a single case"""
        response = self.client.get(f"/api/cases/{self.case.case_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["case_number"], "123456")

    def test_create_case(self):
        """Test creation case"""
        data = {
            "case_number": "789101",
            "crime_type": "Fraud",
            "created_by": self.user.id,
        }
        response = self.client.post("/api/cases/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["case_number"], "789101")

    def test_update_case(self):
        """Test update case"""
        data = {"crime_type": "Updated Theft"}
        response = self.client.put(f"/api/cases/{self.case.case_id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["crime_type"], "Updated Theft")

    def test_delete_case(self):
        """Test Deletion Case"""
        response = self.client.delete(f"/api/cases/{self.case.case_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Case.objects.filter(case_id=self.case.case_id).exists())

    def test_assign_user_to_case(self):
        """Test assigning users to cases"""
        new_user = User.objects.create(username="testuser2")
        response = self.client.post(
            f"/api/cases/{self.case.case_id}/assign-user/", {"user_id": new_user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(new_user, self.case.assigned_users.all())

    def test_remove_user_from_case(self):
        """Test removing a user from a case"""
        new_user = User.objects.create(username="testuser2")
        self.case.assigned_users.add(new_user)
        response = self.client.post(
            f"/api/cases/{self.case.case_id}/remove-user/", {"user_id": new_user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(new_user, self.case.assigned_users.all())
