from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('patients/', views.patients_view, name='patients'),
    path('doctors/', views.doctors_view, name='doctors'),
    path('mappings/', views.mappings_view, name='mappings'),
]
