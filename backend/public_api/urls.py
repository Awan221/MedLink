from django.urls import path
from . import views

urlpatterns = [
    # URLs existantes
    path('appointments/', views.PublicAppointmentView.as_view(), name='public-appointments'),
    path('donors/', views.PublicDonorView.as_view(), name='public-donors'),
    path('contact/', views.PublicContactView.as_view(), name='public-contact'),
    
    # URLs pour les maladies
    path('diseases/', views.DiseaseList.as_view(), name='disease-list'),
    path('diseases/search/', views.DiseaseSearchView.as_view(), name='disease-search'),
    path('diseases/categories/', views.DiseaseCategoryList.as_view(), name='disease-categories'),
    path('diseases/<slug:slug>/', views.DiseaseDetail.as_view(), name='disease-detail'),
]
