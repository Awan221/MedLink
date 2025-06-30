from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'studies', views.DICOMStudyViewSet, basename='dicom-study')
router.register(r'series', views.DICOMSeriesViewSet, basename='dicom-series')
router.register(r'instances', views.DICOMInstanceViewSet, basename='dicom-instance')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoint pour la recherche dans le PACS
    path('pacs/search/', views.DICOMStudyViewSet.as_view({'post': 'search_pacs'}), name='pacs-search'),
    
    # Endpoint pour la visualisation OHIF
    path('viewer/', views.OHIFViewerAPIView.as_view(), name='ohif-viewer'),
]
