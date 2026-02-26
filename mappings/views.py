from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import PatientDoctorMapping
from .serializers import MappingSerializer, MappingDetailSerializer


class MappingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.all()
        serializer = MappingDetailSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MappingSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.validated_data['patient']
            doctor = serializer.validated_data['doctor']
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
                return Response(
                    {'error': 'This doctor is already assigned to this patient.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingByPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id)
        if not mappings.exists():
            return Response(
                {'message': 'No doctors assigned to this patient.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MappingDetailSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MappingDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        mapping.delete()
        return Response(
            {'message': 'Mapping removed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
