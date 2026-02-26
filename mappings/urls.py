from django.urls import path
from .views import MappingListCreateView, MappingByPatientView, MappingDeleteView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
    path('patient/<int:patient_id>/', MappingByPatientView.as_view(), name='mapping-by-patient'),
]
