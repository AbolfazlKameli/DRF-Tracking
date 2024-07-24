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

    def test_writers_url(self):
        url = reverse('home:writers')
        self.assertEqual(resolve(url).func.view_class, views.WriterListView)

    def test_writer_url(self):
        url = reverse('home:writer_detail', args=[13])
        self.assertEqual(resolve(url).func.view_class, views.WriterDetailView)
