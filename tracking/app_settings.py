class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default=None):
        from django.conf import settings

        return getattr(settings, f'{self.prefix}_{name}', default)

    @property
    def PATH_LENGTH(self):
        return self._setting('PATH_LENGTH', 200)

    @property
    def VIEW_LENGTH(self):
        return self._setting('VIEW_LENGTH', 200)

    @property
    def VIEW_METHOD_LENGTH(self):
        return self._setting('VIEW_METHOD_LENGTH', 200)


app_settings = AppSettings('DRF_TRACKING')
