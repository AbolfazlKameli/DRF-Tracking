from django.urls import path
from . import views

urlpatterns = [
    path('no-logging/', views.MockNoLoggingAPI.as_view(), name='no-logging'),
    path('logging/', views.MockLoggingAPI.as_view(), name='logging'),
]
