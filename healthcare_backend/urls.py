"""
URL configuration for healthcare_backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── API endpoints ────────────────────────────────────────────────
    path('api/auth/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),

    # ── DRF browsable API login (optional convenience) ───────────────
    path('api-auth/', include('rest_framework.urls')),

    # ── Frontend (HTML pages) ────────────────────────────────────────
    path('', include('frontend.urls')),
]
