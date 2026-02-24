from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Quiz, Resource


class PageAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')

    def test_sessions_library_login_required(self):
        # authenticated user should access pages
        resp = self.client.get(reverse('sessions'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('library'))
        self.assertEqual(resp.status_code, 200)

    def test_sessions_shows_user_quizzes(self):
        # create quiz belonging to user and ensure it appears
        Quiz.objects.create(title='Test', description='d', created_by=self.user)
        resp = self.client.get(reverse('sessions'))
        self.assertContains(resp, 'Test')

    def test_library_shows_resources_and_quizzes(self):
        quiz = Quiz.objects.create(title='Quiz1', description='desc', created_by=self.user)
        Resource.objects.create(title='Res1', description='desc', created_by=self.user)
        resp = self.client.get(reverse('library'))
        self.assertContains(resp, 'Quiz1')
        self.assertContains(resp, 'Res1')
