from rest_framework import generics
from .models import PrescriptionHistory
from .serializers import PrescriptionHistorySerializer

class PrescriptionHistoryList(generics.ListAPIView):
    serializer_class = PrescriptionHistorySerializer

    def get_queryset(self):
        prescription_id = self.kwargs['prescription_id']
        return PrescriptionHistory.objects.filter(prescription__id=prescription_id).order_by('-performed_at')
