import ast
import ipaddress
import logging
import traceback

from django.utils.timezone import localtime

from .app_settings import app_settings

logger = logging.getLogger(__name__)


class BaseLoggingMixin:
    logging_methods = '__all__'
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '***************'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'cleaned substitute must be string.'
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self.info = {'requested_at': localtime()}
        if not getattr(self, 'decode_request_body', app_settings.DECODE_REQUEST_BODY):
            self.info['data'] = ''
        else:
            self.info['data'] = request.data
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.info['errors'] = traceback.format_exc()
        return response

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        if self.should_log(request, response):
            user = self._get_user(request)
            if response.streaming:
                rendered_content = None
            elif hasattr(response, 'rendered_content'):
                rendered_content = response.rendered_content
            else:
                rendered_content = response.getvalue()
            self.info.update({
                'remote_addr': self._get_ip_address(request),
                'view': self._get_view_name(request),
                'view_method': self._get_view_method(request),
                'path': self._get_path(request),
                'host': request.get_host(),
                'method': request.method,
                'user': user,
                'username_persistent': user.get_username() if user is not None else 'AnonymousUser',
                'response_ms': self._get_response_time(),
                'status_code': response.status_code,
                'query_params': self._clean_data(request.query_params.dict()),
                'response': self._clean_data(rendered_content)
            })
            try:
                self.handle_info()
            except Exception:
                logger.exception('info handler raised this exception!')
        return response

    def handle_info(self):
        raise NotImplementedError

    def _get_ip_address(self, request):
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR')
        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR').split(',')[0]

        possibles = (ipaddr.lstrip('[').split(']')[0], ipaddr.split(':')[0])

        for addr in possibles:
            try:
                return str(ipaddress.ip_address(addr))
            except:
                pass

        return ipaddr

    def _get_view_name(self, request):
        method = request.method.lower()
        try:
            attr = getattr(self, method)
            return (type(attr.__self__).__module__ + "." + type(attr.__self__).__name__)[:app_settings.VIEW_LENGTH]
        except AttributeError:
            return None

    def _get_view_method(self, request):
        action = None
        if hasattr(self, 'action'):
            action = self.action
        return request.method.lower(), action

    def _get_path(self, request):
        return request.path[:app_settings.PATH_LENGTH]

    def _get_user(self, request):
        return None if request.user.is_anonymous else request.user

    def _get_response_time(self):
        response_timedelta = localtime() - self.info['requested_at']
        response_ms = int(response_timedelta.total_seconds() * 1000)
        return max(response_ms, 0)

    def should_log(self, request, response):
        return (
                self.logging_methods == '__all__' or request.method in self.logging_methods
        )

    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='replace')

        if isinstance(data, list):
            return [self._clean_data(d) for d in data]

        if isinstance(data, dict):
            SENSITIVE_FIELDS = {'api', 'token', 'key', 'secret', 'password', 'signature'}
            if self.sensitive_fields:
                SENSITIVE_FIELDS = SENSITIVE_FIELDS | {field.lower() for field in self.sensitive_fields}

            for key, value in data.items():
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass

                if isinstance(value, (list, dict)):
                    data[key] = self._clean_data(value)
                if key.lower() in SENSITIVE_FIELDS:
                    data[key] = self.CLEANED_SUBSTITUTE
        return data
