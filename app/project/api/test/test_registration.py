from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


User = get_user_model()


class RegistrationTest(TestCase):
    endpoint = 'api:registration_view'
    methods = ['POST']

    def test_no_email_sent(self):
        self.response = self.client.get(reverse('api:registration_view'))
        self.assertEqual(len(mail.outbox), 0)

    def test_email_sent(self):
        response = self.client.post(reverse('api:registration_view'), {'email': 'test@example.com'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(User.objects.get(email='test@example.com'))
        new_user = User.objects.get(email='test@example.com')
        self.assertIsNotNone(new_user.user_profile)
        self.assertIsNotNone(new_user.user_profile.registration_code)
        self.assertIn(new_user.user_profile.registration_code, mail.outbox[0].body)

    def test_email_wrong(self):
        response = self.client.post(reverse('api:registration_view'), {'email': 'testexample.com'})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data.get('email'))

    def test_email_already_exists(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        response = self.client.post(reverse('api:registration_view'), {'email': 'lennon@thebeatles.com'})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User with this email address already exists', response.data.get('email'))


class RegistrationValidationTest(TestCase):
    endpoint = 'api:registration_validation_view'
    methods = ['POST']

    def test_wrong_code(self):
        response = self.client.post(reverse(self.endpoint), {'code': 'xxxxx'})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Wrong validation code or already validated!', response.data.get('code'))

    def test_required_fields(self):
        response = self.client.post(reverse('api:registration_validation_view'))
        fields = ['first_name', 'last_name', 'password', 'password_repeat']
        for field in fields:
            self.assertIn('This field is required.', response.data.get(field))
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_fields(self):
        fields = ['first_name', 'last_name', 'password', 'password_repeat']
        data = {k: '' for k in fields}
        response = self.client.post(reverse('api:registration_validation_view'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in fields:
            self.assertIn('This field may not be blank.', response.data.get(field))

    def test_wrong_repeat_pw(self):
        # fields = ['password', 'repeat_password']
        data = {'password': 'pw1', 'repeat_password': 'pw2'}
        response = self.client.post(reverse('api:registration_validation_view'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        if response.data.get('pw1') and response.data.get('pw2'):
            self.assertIn('Passwords don\'t match', response.data.get('password'))
