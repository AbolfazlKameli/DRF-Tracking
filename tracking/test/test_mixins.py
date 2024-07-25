from django.urls import reverse
from rest_framework.test import APITestCase

from tracking.models import APIRequestLog


class TestLoggingMixin(APITestCase):
    def test_no_logging(self):
        self.client.get(reverse('tracking:no-logging'))
        self.assertEqual(APIRequestLog.objects.all().count(), 0)

    def test_logging(self):
        self.client.get(reverse('tracking:logging'))
        self.assertEqual(APIRequestLog.objects.all().count(), 1)
