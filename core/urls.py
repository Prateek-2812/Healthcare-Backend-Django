from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    PatientListCreateView,
    PatientDetailView,
    DoctorListCreateView,
    DoctorDetailView,
    PatientDoctorMappingListCreateView,
    PatientDoctorMappingDetailView,
)

urlpatterns = [
    # Authentication
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),

    # Patient management
    path("patients/", PatientListCreateView.as_view(), name="patient-list-create"),
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),

    # Doctor management
    path("doctors/", DoctorListCreateView.as_view(), name="doctor-list-create"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),

    # Patient-doctor mappings
    path("mappings/", PatientDoctorMappingListCreateView.as_view(), name="mapping-list-create"),
    path("mappings/<int:pk>/", PatientDoctorMappingDetailView.as_view(), name="mapping-detail"),
]


