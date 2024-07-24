import ipaddress
import traceback

from django.utils.timezone import localtime

from .app_settings import app_settings


class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        self.info = {'requested_at': localtime()}
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.info['errors'] = traceback.format_exc()
        return response

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        user = self._get_user(request)
        self.info.update({
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'path': self._get_path(request),
            'host': request.get_host(),
            'method': request.method,
            'user': user,
            'username_persistent': user.get_username() if user else 'AnonymousUser',
            'response_ms': self._get_response_time(),
            'status_code': response.status_code,
        })
        self.handle_info()
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
        if hasattr(self, 'action'):
            return self.action[:app_settings.VIEW_METHOD_LENGTH]
        return request.method.lower()[:app_settings.VIEW_METHOD_LENGTH]

    def _get_path(self, request):
        return request.path[:app_settings.PATH_LENGTH]

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def _get_response_time(self):
        response_timedelta = localtime() - self.info['requested_at']
        response_ms = int(response_timedelta.total_seconds() * 1000)
        return max(response_ms, 0)
