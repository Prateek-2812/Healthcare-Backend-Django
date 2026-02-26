from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization', 'experience_years', 'created_by']
    search_fields = ['name', 'specialization']
    list_filter = ['specialization']
