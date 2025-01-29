from django.test import SimpleTestCase
from django.urls import reverse, resolve
from case_api.views import upload_file, list_files

class UrlsTest(SimpleTestCase):
    def test_upload_file_url_resolves(self):
        url = reverse('upload_file')
        self.assertEqual(resolve(url).func, upload_file)

    def test_list_files_url_resolves(self):
        url = reverse('list_files')
        self.assertEqual(resolve(url).func, list_files)
