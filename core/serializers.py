from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Patient, Doctor, PatientDoctorMapping


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Expects: name, email, password
    """

    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        read_only_fields = ('id',)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # Use email as username; store name in first_name for simplicity
        user = User(
            username=email,
            email=email,
            first_name=name,
        )
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Simple serializer to validate login payload.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient CRUD.
    The authenticated user is automatically set as created_by.
    """

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "address",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor CRUD.
    """

    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "email",
            "specialization",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for patient-doctor mappings.
    """

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient",
            "doctor",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


