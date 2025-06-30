from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AIModelViewSet, AIPredictionViewSet, AIAlertViewSet
)

router = DefaultRouter()
router.register(r'models', AIModelViewSet)
router.register(r'predictions', AIPredictionViewSet)
router.register(r'alerts', AIAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]