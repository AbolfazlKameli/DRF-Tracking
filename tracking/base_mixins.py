import ipaddress

from django.utils.timezone import now

from .app_settings import app_settings


class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        self.info = {'requested_at': now()}
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self.info.update({
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'path': self._get_path(request),
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
