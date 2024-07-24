from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/<str:username>/', views.AboutView.as_view(), name='about'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('writers/', views.WriterListView.as_view(), name='writers'),
    path('writer/<int:id>/', views.WriterDetailView.as_view(), name='writer_detail'),
]
