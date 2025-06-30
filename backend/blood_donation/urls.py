from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BloodCenterViewSet, BloodDonationAlertViewSet

router = DefaultRouter()
router.register(r'centers', BloodCenterViewSet)
router.register(r'alerts', BloodDonationAlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
] 