from django.urls import path, include

from . import views

app_name = 'tracking'
urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('test/', include('tracking.test.urls')),
]
