from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'phone', 'email',
                  'experience_years', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
