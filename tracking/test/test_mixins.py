from django.test import override_settings
from rest_framework.test import APITestCase, APIRequestFactory

from tracking.models import APIRequestLog
from . import views


@override_settings(ROOT_URLCONF='tracking.test.urls')
class TestLoggingMixin(APITestCase):
    def test_no_logging(self):
        self.client.get('/no-logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 0)

    def test_logging(self):
        self.client.get('/logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 1)
