from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('KhatMan/', admin.site.urls),
    path('', include('tracking.urls', namespace='tracking')),
]
