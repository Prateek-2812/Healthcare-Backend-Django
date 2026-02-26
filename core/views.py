from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Payload: { "name": "...", "email": "...", "password": "..." }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "name": user.first_name,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/auth/login/
    Payload: { "email": "...", "password": "..." }
    Returns: JWT access and refresh tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = authenticate(request, username=user.username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class PatientListCreateView(generics.ListCreateAPIView):
    """
    POST /api/patients/ - create patient (current user as owner)
    GET /api/patients/ - list patients created by current user
    """

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/patients/<id>/
    PUT /api/patients/<id>/
    DELETE /api/patients/<id>/
    Only allows access to patients owned by the current user.
    """

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    POST /api/doctors/
    GET /api/doctors/
    """

    queryset = Doctor.objects.all().order_by("name")
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/doctors/<id>/
    PUT /api/doctors/<id>/
    DELETE /api/doctors/<id>/
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    """
    POST /api/mappings/ - assign doctor to patient
    GET /api/mappings/ - list all mappings
    """

    queryset = PatientDoctorMapping.objects.select_related("patient", "doctor")
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        # Ensure the current user owns the patient they are mapping
        if patient.created_by != self.request.user:
            return Response(
                {"detail": "You cannot assign doctors to patients you do not own."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()


class PatientDoctorMappingDetailView(APIView):
    """
    GET /api/mappings/<pk>/ - list doctors assigned to a patient where pk = patient_id
    DELETE /api/mappings/<pk>/ - remove a mapping where pk = mapping_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        doctors = Doctor.objects.filter(patient_mappings__patient_id=pk).distinct()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
            mapping.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"detail": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

