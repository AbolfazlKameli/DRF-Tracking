from django.contrib.auth.models import User
from django.test import TestCase

from home import forms


class TestRegistrationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='username', email='email@gmail.com', password='password')

    def test_valid_data(self):
        data = {'username': 'abolfazl', 'email': 'abolfazl@gamil.com', 'password': 'password', 'password2': 'password'}
        form = forms.RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        data = {}
        form = forms.RegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = {'username': 'test', 'email': 'email@gmail.com', 'password': 'password', 'password2': 'password'}
        form = forms.RegisterForm(data=data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_invalid_username(self):
        data = {'username': 'username', 'email': 'abolfazl@gmail.com', 'password': 'password', 'password2': 'password'}
        form = forms.RegisterForm(data=data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))

    def test_invalid_password(self):
        data = {'username': 'abolfazl', 'email': 'abolfazl@gamil.com', 'password': 'pass', 'password2': 'password'}
        form = forms.RegisterForm(data=data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
