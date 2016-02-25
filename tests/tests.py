import pyclamd, tempfile
from django.test import TestCase, Client
from clamav_upload.models import AllowedContentType

class AllowedContentTypeTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.cd = pyclamd.ClamdAgnostic()
        self.no_eicar = tempfile.NamedTemporaryFile()
        self.no_eicar.write('no virus in this file')
        self.no_eicar.flush()
        self.no_eicar.seek(0)
        self.eicar = tempfile.NamedTemporaryFile()
        self.eicar.write(self.cd.EICAR())
        self.eicar.flush()
        self.eicar.seek(0)
        self.allowed_type = AllowedContentType(
            allowed_type='text/plain')
        self.allowed_type.save()

    def tearDown(self):
        self.eicar.close()
        self.no_eicar.close()
        try:
            self.allowed_type.delete()
        except AssertionError:
            pass

    def test_eicar(self):
        eicar = self.cd.scan_stream(self.eicar.read())
        no_eicar = self.cd.scan_stream(self.no_eicar.read())
        self.assertEqual(eicar.get(
            'stream', None), ('FOUND', 'Eicar-Test-Signature'))
        self.assertEqual(no_eicar, None)

    def test_disallowed_content_types(self):
        self.allowed_type.delete()
        self.assertEqual(
            self.client.post('/upload/', {'file': self.no_eicar}).status_code, 403)
        
    def test_upload_allowed_content_types(self):
        self.assertEqual(
            self.client.post('/upload/', {'file': self.no_eicar}).status_code, 200)

    def test_upload_virus_signature_detection(self):
        self.assertEqual(
            self.client.post('/upload/', {'file': self.eicar}).status_code, 403)
