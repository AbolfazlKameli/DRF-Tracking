from django.test import SimpleTestCase
from django.urls import reverse, resolve

from home import views


class TestUrls(SimpleTestCase):
    def test_home_url(self):
        url = reverse('home:home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_register_url(self):
        url = reverse('home:register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterView)

    def test_about_url(self):
        url = reverse('home:about', args=['username'])
        self.assertEqual(resolve(url).func.view_class, views.AboutView)
