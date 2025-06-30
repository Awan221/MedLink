from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalRecordViewSet, PrescriptionViewSet, AppointmentViewSet
from .views_history import MedicalRecordHistoryList, PatientHistoryList
from .views_prescription_history import PrescriptionHistoryList

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:patient_id>/medical-records/', MedicalRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='patient-medical-records'),
    path('<uuid:patient_id>/medical-records/<int:pk>/', MedicalRecordViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='patient-medical-record-detail'),
    path('<uuid:patient_id>/prescriptions/', PrescriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='patient-prescriptions'),
    path('<uuid:patient_id>/prescriptions/<int:pk>/', PrescriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='patient-prescription-detail'),
    path('medical-records/<int:medical_record_id>/history/', MedicalRecordHistoryList.as_view(), name='medicalrecord-history'),
    path('<uuid:patient_id>/history/', PatientHistoryList.as_view(), name='patient-history'),
    path('prescriptions/<int:prescription_id>/history/', PrescriptionHistoryList.as_view(), name='prescription-history'),
]