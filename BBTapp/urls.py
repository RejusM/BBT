from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Pagrindinis puslapis
    path('register/', views.register, name='register'),  # Registracija
    path('profile/', views.profile, name='profile'),  # Profilio puslapis
]
