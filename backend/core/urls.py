from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
   openapi.Info(
      title="Orthanc Telemedicine API",
      default_version='v1',
      description="API Documentation for Orthanc Telemedicine Platform",
      terms_of_service="https://www.orthanc-telemedicine.com/terms/",
      contact=openapi.Contact(email="contact@orthanc-telemedicine.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/dicom/', include('dicom.urls')),  # API DICOM pour la téléradiologie
    path('api/imaging/', include('imaging.urls')),  # API pour la gestion des études d'imagerie
    path('api/blood-bank/', include('bloodbank.urls')),  # API pour la banque de sang
    path('api/chatbot/', include('chatbot.urls')),
    path('api/public/', include('public_api.urls')),  # API publique pour le portail
    
    # Catch-all pour le frontend SPA (doit être la dernière URL)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='frontend')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Ajout du dossier static pour le développement
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns