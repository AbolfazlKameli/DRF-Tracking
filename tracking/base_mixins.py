class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, *args, **kwargs):
        return super().finalize_response(request, *args, **kwargs)
