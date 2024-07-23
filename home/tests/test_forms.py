from django.contrib.auth.models import User
from django.test import TestCase

from home import forms


class TestRegistrationForm(TestCase):
    def test_valid_data(self):
        data = {'username': 'abolfazl', 'email': 'abolfazl@gamil.com', 'password': 'testpass', 'password2': 'testpass'}
        form = forms.RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        data = {}
        form = forms.RegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        User.objects.create_user(username='abolfazl', email='test@gmail.com', password='<PASSWORD>')
        data = {'username': 'test', 'email': 'test@gmail.com', 'password': 'testpass', 'password2': 'testpass'}
        form = forms.RegisterForm(data=data)
        self.assertTrue(form.has_error('email'))

    def test_invalid_username(self):
        User.objects.create_user(username='test', email='test@gmail.com', password='<PASSWORD>')
        data = {'username': 'test', 'email': 'abolfazl@gmail.com', 'password': 'testpass', 'password2': 'testpass'}
        form = forms.RegisterForm(data=data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))

    def test_invalid_password(self):
        data = {'username': 'abolfazl', 'email': 'abolfazl@gamil.com', 'password': 'pass', 'password2': 'testpass'}
        form = forms.RegisterForm(data=data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
