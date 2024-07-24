from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from model_bakery import baker

from home import models
from home import views
from home.forms import RegisterForm


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('home:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/register.html')
        self.failUnless(response.context['form'], RegisterForm)

    def test_user_register_valid_POST(self):
        data = {'username': 'username', 'email': 'email@gmail.com', 'password': 'password', 'password2': 'password'}
        response = self.client.post(reverse('home:register'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_invalid_POST(self):
        data = {'username': 'username', 'email': 'email', 'password': 'password', 'password2': 'password'}
        response = self.client.post(reverse('home:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='email', errors=['Enter a valid email address.'])


class TestWriterDetailView(TestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True)
        self.factory = RequestFactory()

    def test_authenticated_user(self):
        request = self.factory.get(reverse('home:writer_detail', kwargs={'id': 1}))
        request.user = self.user
        response = views.WriterDetailView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_not_authenticated_user(self):
        request = self.factory.get(reverse('home:writer_detail', kwargs={'id': 1}))
        request.user = AnonymousUser()
        response = views.WriterDetailView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class TestWritersView(TestCase):
    def setUp(self):
        User.objects.create_user(username='username', email='email@gmail.com', password='password')
        self.client = Client()
        self.client.login(username='username', email='email@gmail.com', password='password')

    def test_writers_GET(self):
        response = self.client.get(reverse('home:writers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/writers.html')
