from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'centers', views.BloodDonationCenterViewSet, basename='blood-center')
router.register(r'inventory', views.BloodInventoryViewSet, basename='blood-inventory')
router.register(r'donations', views.BloodDonationViewSet, basename='blood-donation')

urlpatterns = [
    path('', include(router.urls)),
    
    # Statistiques et rapports
    path('stats/summary/', views.BloodInventoryViewSet.as_view({'get': 'summary'}), name='blood-inventory-summary'),
    path('stats/donations/', views.BloodDonationViewSet.as_view({'get': 'stats'}), name='blood-donation-stats'),
    
    # Points de collecte proches
    path('centers/near-me/', views.BloodDonationCenterViewSet.as_view({'get': 'near_me'}), name='blood-centers-near-me'),
    
    # Traitement des dons
    path('donations/<uuid:pk>/process/', 
         views.BloodDonationViewSet.as_view({'post': 'process'}), 
         name='blood-donation-process'),
]
