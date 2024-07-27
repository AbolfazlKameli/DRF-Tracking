from django.urls import path

from . import views as test_views

urlpatterns = [
    path('no-logging/', test_views.MockNoLoggingAPI.as_view(), name='no-logging'),
    path('logging/', test_views.MockLoggingAPI.as_view(), name='logging'),
    path('explicit-logging/', test_views.MockExplicitLoggingAPI.as_view(), name='explicit-logging'),
    path('custom-check-logging/', test_views.MockCustomCheckLoggingAPI.as_view(), name='custom-check-logging'),
    path('session-auth-logging/', test_views.MockSessionAuthLoggingAPI.as_view(), name='session-auth-logging'),
    path('token-auth-logging/', test_views.MockTokenAuthLoggingAPI.as_view(), name='token-auth-logging'),
    path('sensitive-fields-logging/', test_views.MockSensitiveFieldsLoggingAPI.as_view(),
         name='sensitive-fields-logging'),
    path('invalid-cleaned-logging/', test_views.MockInvalidCleanedSubstituteLoggingAPI.as_view(),
         name='invalid-cleaned-logging'),
]
