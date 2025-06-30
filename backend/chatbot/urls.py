from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatbotKnowledgeBaseViewSet, ChatSessionViewSet, 
    ChatMessageViewSet, ChatFeedbackViewSet,
    chat_request, submit_feedback, ChatSessionCreateView
)

# Configuration du routeur principal
router = DefaultRouter()
router.register(r'knowledge', ChatbotKnowledgeBaseViewSet, basename='knowledge')
router.register(r'messages', ChatMessageViewSet, basename='messages')
router.register(r'feedback', ChatFeedbackViewSet, basename='feedback')

# Configuration spécifique pour les sessions
session_router = DefaultRouter()
session_router.register(r'', ChatSessionViewSet, basename='sessions')

urlpatterns = [
    # Inclure les routes du routeur principal
    path('', include(router.urls)),
    
    # Routes personnalisées pour le chat
    path('request/', chat_request, name='chat-request'),
    path('feedback/', submit_feedback, name='submit-feedback'),
    
    # Routes pour les sessions
    path('session/', ChatSessionCreateView.as_view(), name='create-session'),
    path('sessions/<uuid:session_id>/messages/', ChatMessageViewSet.as_view({'get': 'list'}), name='session-messages'),
    
    # Inclure les routes du routeur des sessions
    path('sessions/', include(session_router.urls)),
    
    # Alias pour la compatibilité avec les anciennes URLs
    path('sessions/<uuid:pk>/', ChatSessionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='session-detail'),
]