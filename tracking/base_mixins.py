import ipaddress

from django.utils.timezone import now


class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        self.info = {'requested_at': now()}
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self.info.update({
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
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
            attribute = getattr(self, method)
            return type(attribute.__self__).__module__ + "." + type(attribute.__self__).__name__
        except AttributeError:
            return None
