import ast

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase, APIRequestFactory

from tracking.base_mixins import BaseLoggingMixin
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

    def test_info_path(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.path, '/logging/')

    # Ip Address
    def test_info_ip_remote(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.196'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.196')

    def test_info_ip_remote_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.196, 128.1.1.98'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.196')

    def test_info_ip_remote_v4_with_port(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.196:8000'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.196')

    def test_info_ip_remote_v6(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '2001:0000:130F:0000:0000:09C0:876A:130B'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '2001:0:130f::9c0:876a:130b')

    def test_info_ip_remote_v6_loopback(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '::1'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')

    def test_info_ip_remote_v6_with_port(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '[::1]:8569'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')

    # x_forwarded
    def test_info_ip_xforwaded(self):
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.196'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.196')

    def test_info_ip_xforwaded_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.196, 128.1.1.98'
        views.MockLoggingAPI.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.196')

    # Host
    def test_info_host(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.host, 'testserver')

    # Method
    def test_info_method(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.method, 'GET')

    def test_info_status_code_OK(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.status_code, 200)

    def test_info_status_code_METHOD_NOT_ALLOWED(self):
        self.client.post('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.status_code, 405)

    def test_logging_explicit(self):
        self.client.get('/explicit-logging/')
        self.client.post('/explicit-logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    def test_custom_check_logging(self):
        self.client.get('/custom-check-logging/')
        self.client.post('/custom-check-logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    def test_anon_user(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, None)

    def test_auth_user(self):
        user = User.objects.create_user(username='username', password='password')

        self.client.login(username='username', password='password')
        self.client.get('/session-auth-logging/')

        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, user)

    def test_params(self):
        self.client.get('/logging/', {'p1': 'test', 'another': '32'})
        log = APIRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {'p1': 'test', 'another': '32'})

    def test_param_cleaned(self):
        self.client.get('/sensitive-fields-logging/', {'myfield': 'this is a text', 'api': 'test', 'test': 'test'})
        log = APIRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {
            'myfield': BaseLoggingMixin.CLEANED_SUBSTITUTE,
            'api': BaseLoggingMixin.CLEANED_SUBSTITUTE,
            'test': 'test'
        })

    def test_invalid_cleaned_substitute(self):
        with self.assertRaises(AssertionError):
            self.client.get('/invalid-cleaned-logging/')
