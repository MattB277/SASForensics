from django.test import TestCase
from case_api.utils import upload_to_based_on_type

class UtilsTest(TestCase):
    def test_upload_to_based_on_type(self):
        class MockInstance:
            pass
        path = upload_to_based_on_type(MockInstance(), "example.pdf")
        self.assertEqual(path, "pdfs/example.pdf")
