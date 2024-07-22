from django.test import SimpleTestCase
from home.views import HomeView, AboutView
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('home:home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_about(self):
        url = reverse('home:about', args=['username'])
        self.assertEqual(resolve(url).func.view_class, AboutView)
