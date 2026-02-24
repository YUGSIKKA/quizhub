from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p', email='u@example.com')
        self.client.login(username='u', password='p')

    def test_profile_and_settings_pages(self):
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Username:')

        resp = self.client.get(reverse('settings'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Settings')

    def test_settings_form_updates_user(self):
        data = {'username': 'newname', 'email': 'new@example.com'}
        resp = self.client.post(reverse('settings'), data)
        self.assertRedirects(resp, reverse('settings'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newname')
        self.assertEqual(self.user.email, 'new@example.com')
