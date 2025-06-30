from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BloodBankCenterViewSet, BloodStockViewSet, 
    BloodDonationViewSet, BloodRequestViewSet
)

router = DefaultRouter()
router.register(r'centers', BloodBankCenterViewSet)
router.register(r'stocks', BloodStockViewSet)
router.register(r'donations', BloodDonationViewSet)
router.register(r'requests', BloodRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]