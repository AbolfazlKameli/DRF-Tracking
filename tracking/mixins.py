from .base_mixins import BaseLoggingMixin


class LoggingMixin(BaseLoggingMixin):
    def handle_info(self):
        # APIRequestLog(**self.info).save()
        print(self.info)
