from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DicomStudyViewSet, DicomSeriesViewSet, 
    DicomInstanceViewSet, RadiologyReportViewSet, ActionLogViewSet
)
from .views_orthanc import OrthancProxyView

router = DefaultRouter()
router.register(r'studies', DicomStudyViewSet)
router.register(r'reports', RadiologyReportViewSet)
router.register(r'action-logs', ActionLogViewSet, basename='actionlog')

urlpatterns = [
    path('', include(router.urls)),
    path('studies/<uuid:study_id>/series/', DicomSeriesViewSet.as_view({'get': 'list', 'post': 'create'}), name='study-series'),
    path('studies/<uuid:study_id>/series/<uuid:pk>/', DicomSeriesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='study-series-detail'),
    path('series/<uuid:series_id>/instances/', DicomInstanceViewSet.as_view({'get': 'list', 'post': 'create'}), name='series-instances'),
    path('series/<uuid:series_id>/instances/<uuid:pk>/', DicomInstanceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='series-instance-detail'),
    
    # Proxy pour Orthanc
    path('orthanc/<path:path>', OrthancProxyView.as_view(), name='orthanc-proxy'),
    path('orthanc/', OrthancProxyView.as_view(), name='orthanc-proxy-root'),
]