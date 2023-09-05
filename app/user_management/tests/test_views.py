from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

class SignUpTest(TestCase):

    def test_create_new_user(self):
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_existing_username(self):
        User.objects.create_user('existinguser', 'user@example.com', 'password123')
        response = self.client.post(reverse('sign_up'), {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        })
        self.assertContains(response, "User with given username already exists")

    def test_existing_email(self):
        User.objects.create_user('existinguser', 'existing@example.com', 'password123')
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser',
            'email': 'existing@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        })
        self.assertContains(response, "User with given emails already exists")

    def test_password_mismatch(self):
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'pass1': 'password123',
            'pass2': 'password456'
        })
        self.assertContains(response, "Verification of your passwords failed")


class PasswordResetEmailTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')

    def test_send_password_reset_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Check that one message was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify email details
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Password reset on testserver')
        self.assertEqual(email.to, ['test@example.com'])
        self.assertIn("You're receiving this email because you requested a password reset", email.body)
