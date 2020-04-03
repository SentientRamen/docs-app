from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from .models import Document, UserDocumentInfo

# Create your tests here.


class DocsAppTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.username1 = 'testuser1'
        cls.password1 = 'testpassword1'
        cls.email1 = 'test@user1.com'

        # Registering test user
        cls.client.post('/docs/register/', dict(
            username=cls.username1,
            email=cls.email1,
            password1=cls.password1,
            password2=cls.password1,
        ))
        cls.test_user = User.objects.get(username=cls.username1)
        cls.test_document = Document.objects.create(name='testdoc1')

    def test_login(self):
        # Trying login with correct credentials
        response = self.client.post('/docs/login/', dict(
            username=self.username1,
            password=self.password1,
        ))
        # Return the correct template page for document i.e. room.html
        self.assertEqual(response.url, '/docs/')

    def test_when_document_does_not_exist(self):

        # logging in the registered user
        self.client.post('/docs/login/', dict(
            username=self.username1,
            password=self.password1,
        ))
        # Trying to access a document that does not exist, should get a 404 response
        response = self.client.post('/docs/testdoc2/', dict(
            username=self.username1,
        ))

        # Since document does not exist, the view will return a 404 not found response
        self.assertEqual(response.status_code, 404)

    def test_user_authorization_to_access_document(self):

        # logging in the registered user
        self.client.post('/docs/login/', dict(
            username=self.username1,
            password=self.password1,
        ))

        # Trying to access a document that does not have access to yet, should return 403
        response = self.client.post('/docs/testdoc1/', dict(
            username=self.username1,
        ))
        # Since user is unauthorized, we get back a 403 response
        self.assertEqual(response.status_code, 403)

        # Authorizing user to be able to access the given document
        UserDocumentInfo.objects.create(user=self.test_user, document=self.test_document)
        response = self.client.post('/docs/testdoc1/', dict(
            username=self.username1,
        ))
        # Since user is authorized now, we get back a 200 OK response
        self.assertEqual(response.status_code, 200)
