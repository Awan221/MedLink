from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404
import uuid
import logging
from django.conf import settings
from asgiref.sync import sync_to_async
from rest_framework.views import APIView
from django.utils import timezone

# Modèle de chatbot par défaut
CHATBOT_MODEL = 'meta-llama/llama-3-70b-instruct'  # Modèle par défaut

from .models import ChatbotKnowledgeBase, ChatSession, ChatMessage, ChatFeedback
from .serializers import (
    ChatbotKnowledgeBaseSerializer, ChatSessionSerializer, 
    ChatMessageSerializer, ChatFeedbackSerializer,
    ChatRequestSerializer, ChatSessionCreateSerializer
)
from .services.llama_service import LlamaService
from authentication.permissions import IsAdmin
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

class ChatbotKnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = ChatbotKnowledgeBase.objects.all()
    serializer_class = ChatbotKnowledgeBaseSerializer
    permission_classes = [permissions.IsAuthenticated & IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'content', 'keywords']
    ordering_fields = ['category', 'title', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Nécessite une authentification
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_anonymous', 'user']
    ordering_fields = ['started_at', 'last_activity']
    
    def get_permissions(self):
        """
        Instancie et retourne la liste des permissions que cette vue requiert.
        """
        if self.action in ['create', 'retrieve', 'update', 'partial_update']:
            return [permissions.AllowAny()]  # Autoriser création, consultation et mise à jour sans authentification
        return [permission() for permission in self.permission_classes]  # Pour les autres actions, utiliser les permissions définies
    
    def get_queryset(self):
        user = self.request.user
        session_id = self.kwargs.get('pk') or self.kwargs.get('session_id')
        
        # Journalisation pour le débogage
        logger.debug(f"get_queryset - user: {user}, session_id: {session_id}, action: {self.action}")
        
        # Si l'utilisateur est un administrateur, retourner toutes les sessions
        if user.is_staff or (hasattr(user, 'role') and user.role in ['ADMIN', 'SUPER_ADMIN']):
            if session_id:
                return ChatSession.objects.filter(session_id=session_id)
            return ChatSession.objects.all()
            
        # Pour les utilisateurs authentifiés, retourner leurs sessions
        if user.is_authenticated:
            if session_id:
                return ChatSession.objects.filter(session_id=session_id, user=user)
            return ChatSession.objects.filter(user=user)
            
        # Pour les utilisateurs anonymes, ne retourner que la session spécifique demandée
        if session_id:
            return ChatSession.objects.filter(session_id=session_id, user__isnull=True)
            
        return ChatSession.objects.none()
        
    def get_object(self):
        # Surcharge pour gérer correctement la récupération d'une session par son UUID
        try:
            queryset = self.filter_queryset(self.get_queryset())
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            
            if lookup_url_kwarg in self.kwargs:
                session_id = self.kwargs[lookup_url_kwarg]
                logger.debug(f"Recherche de la session avec l'ID: {session_id}")
                
                # Essayer de récupérer la session par son ID
                try:
                    obj = ChatSession.objects.get(session_id=session_id)
                    logger.debug(f"Session trouvée: {obj}")
                    self.check_object_permissions(self.request, obj)
                    return obj
                except ChatSession.DoesNotExist:
                    logger.error(f"Session non trouvée: {session_id}")
                    raise Http404(f"Aucune session ne correspond à l'ID {session_id}")
                
            return super().get_object()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'objet: {str(e)}")
            raise
            
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.debug(f"Mise à jour de la session: {instance.session_id}")
            
            # Mettre à jour la date de dernière activité
            instance.last_activity = timezone.now()
            
            # Mettre à jour le contexte si fourni
            if 'context' in request.data:
                if not isinstance(instance.context, dict):
                    instance.context = {}
                instance.context.update(request.data['context'])
                
            # Sauvegarder les modifications
            instance.save()
            
            # Retourner la réponse avec le sérialiseur
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la session: {str(e)}")
            return Response(
                {"error": "Une erreur est survenue lors de la mise à jour de la session"},
                status=status.HTTP_400_BAD_REQUEST
            )

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Par défaut, nécessite une authentification
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['session', 'message_type']
    ordering_fields = ['sent_at']
    
    def get_permissions(self):
        """
        Instancie et retourne la liste des permissions que cette vue requiert.
        """
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.AllowAny()]  # Autoriser création et lecture sans authentification
        return [permission() for permission in self.permission_classes]  # Pour les autres actions, utiliser les permissions définies
    
    def get_queryset(self):
        user = self.request.user
        session_id = self.kwargs.get('session_id')
        
        if user.is_staff or user.role in ['ADMIN', 'SUPER_ADMIN']:
            if session_id:
                return ChatMessage.objects.filter(session__session_id=session_id)
            return ChatMessage.objects.all()
        
        if session_id:
            return ChatMessage.objects.filter(session__session_id=session_id, session__user=user)
        return ChatMessage.objects.filter(session__user=user)

class ChatFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ChatFeedback.objects.all()
    serializer_class = ChatFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]  # Par défaut, nécessite une authentification
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['message__session', 'rating']
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        """
        Instancie et retourne la liste des permissions que cette vue requiert.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]  # Autoriser la création de feedback sans authentification
        return [permission() for permission in self.permission_classes]  # Pour les autres actions, utiliser les permissions définies

def _get_system_prompt(session):
    """Génère le prompt système en fonction du type de session et du rôle de l'utilisateur"""
    role = session.user_role or 'utilisateur'
    session_type = session.session_type or 'GENERAL'
    
    base_prompt = """Tu es MedLink, un assistant médical intelligent conçu pour aider les professionnels de santé et les patients.
    Tu dois fournir des réponses précises, vérifiées et adaptées à ton interlocuteur.
    """
    
    # Adaptation en fonction du type de session
    if session_type == 'MEDICAL':
        base_prompt += """
        Tu t'adresses à un professionnel de santé. Tu peux utiliser un vocabulaire médical avancé.
        Tu peux fournir des informations détaillées sur les procédures, les diagnostics et les traitements.
        """
    elif session_type == 'TECHNICAL':
        base_prompt += """
        Tu dois fournir une assistance technique sur l'utilisation de la plateforme MedLink.
        Sois précis et fournis des étapes claires pour résoudre les problèmes techniques.
        """
    elif session_type == 'ADMIN':
        base_prompt += """
        Tu assistes un administrateur de la plateforme. Tu peux fournir des informations sur la gestion des utilisateurs,
        les paramètres système et la configuration de la plateforme.
        """
    
    # Adaptation en fonction du rôle de l'utilisateur
    if role in ['DOCTOR', 'NURSE', 'MEDICAL_STAFF']:
        base_prompt += f"""
        L'utilisateur est un professionnel de santé ({role}).
        Tu peux fournir des informations médicales détaillées et des conseils professionnels.
        """
    
    return base_prompt

@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Autorisation explicite pour les utilisateurs non authentifiés
def chat_request(request):
    """
    Endpoint pour envoyer un message au chatbot et recevoir une réponse
    Utilise le modèle Llama 3.3 70B Instruct via OpenRouter
    
    Note sur les autorisations :
    - Cette vue est accessible sans authentification (@permission_classes([permissions.AllowAny]))
    - La gestion des utilisateurs anonymes est gérée dans la fonction _get_or_create_session
    
    Méthode: POST
    Paramètres:
    - session_id: ID de session existant (optionnel)
    - message: Message de l'utilisateur (obligatoire)
    - session_type: Type de session ('GENERAL', 'MEDICAL', 'TECHNICAL', 'ADMIN') (optionnel, par défaut: 'GENERAL')
    
    Retourne:
    - session_id: ID de la session
    - message_id: ID du message de la réponse
    - response: Réponse du chatbot
    - context: Contexte de la session mis à jour
    - session_type: Type de session actuel
    - user_role: Rôle de l'utilisateur (si disponible)
    - timestamp: Horodatage de la réponse
    - model: Modèle utilisé pour la génération
    - usage: Informations sur l'utilisation du modèle
    """
    # Vérifier si la requête est une requête OPTIONS (prévol CORS)
    if request.method == 'OPTIONS':
        response = Response({}, status=status.HTTP_200_OK)
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    # Validation des données d'entrée
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Validation des données échouée: {serializer.errors}")
        return Response(
            {'errors': serializer.errors, 'status': 'error'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    session_id = data.get('session_id')
    message = data.get('message', '').strip()
    
    # Gestion de l'utilisateur (authentifié ou anonyme)
    user = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
    
    # Si pas de session_id, créer une nouvelle session
    if not session_id:
        try:
            # Créer une nouvelle session avec le type fourni ou 'GENERAL' par défaut
            session_type = data.get('session_type', 'GENERAL')
            session = _get_or_create_session(None, user, session_type)
            session_id = str(session.session_id)
            logger.info(f"Nouvelle session créée pour la requête: {session_id}")
        except Exception as e:
            logger.error(f"Erreur lors de la création d'une nouvelle session: {str(e)}", exc_info=True)
            return Response(
                {'error': f"Impossible de créer une nouvelle session: {str(e)}", 'status': 'error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Vérifier que le message n'est pas vide
    if not message:
        return Response(
            {'error': 'Le message ne peut pas être vide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        logger.info(f"Nouveau message reçu - Session: {session_id}, Utilisateur: {user.id if user else 'Anonyme'}")
        
        # Récupérer ou créer la session avec le type spécifié
        session_type = data.get('session_type', 'GENERAL')
        session = _get_or_create_session(
            session_id=session_id,
            user=user,
            session_type=session_type
        )
        
        # Mettre à jour le contexte de la session
        context = session.context or {}
        if not isinstance(context, dict):
            context = {}
            
        # Initialiser les champs du contexte si nécessaire
        if 'previous_questions' not in context:
            context['previous_questions'] = []
        if 'medical_context' not in context:
            context['medical_context'] = {}
            
        # Ajouter la question actuelle à l'historique (limité à 5)
        context['previous_questions'].append(message)
        if len(context['previous_questions']) > 5:
            context['previous_questions'] = context['previous_questions'][-5:]
        
        # Mettre à jour le type de session et le rôle dans le contexte
        context['session_type'] = session_type
        if user and hasattr(user, 'role') and user.role:
            context['user_role'] = user.role.name.lower()
        
        # Mettre à jour la session avec le nouveau contexte
        session.context = context
        session.save(update_fields=['context', 'last_activity'])
        
        # Enregistrer le message de l'utilisateur avec métadonnées
        user_message = ChatMessage.objects.create(
            session=session,
            content=message,
            message_type='USER',
            metadata={
                'session_type': session_type,
                'user_role': context.get('user_role'),
                'context': context
            }
        )
        logger.debug(f"Message utilisateur enregistré - ID: {user_message.id}")
        
        # Préparer l'historique de conversation pour le modèle
        messages = []
        
        # Ajouter le prompt système avec le contexte
        system_prompt = _get_system_prompt(session)
        messages.append({
            'role': 'system',
            'content': system_prompt
        })
        
        # Ajouter l'historique des messages (limité à 5 derniers échanges)
        chat_history = _get_chat_history(session, limit=5)
        for msg in chat_history:
            messages.append({
                'role': 'user' if msg.message_type == 'USER' else 'assistant',
                'content': msg.content
            })
        
        # Ajouter le message actuel
        messages.append({
            'role': 'user',
            'content': message
        })
        
        # Appeler le service Llama pour obtenir une réponse
        llama_service = LlamaService()
        response = llama_service.get_chat_response(
            messages=messages,
            user_role=context.get('user_role')
        )
        
        # Extraire la réponse de l'assistant
        assistant_message = response['choices'][0]['message']['content'].strip()
        
        try:
            # Enregistrer la réponse de l'assistant
            bot_message = ChatMessage.objects.create(
                session=session,
                content=assistant_message,
                message_type='BOT',
                metadata={
                    'model': CHATBOT_MODEL,
                    'usage': response.get('usage', {}),
                    'session_type': session_type,
                    'user_role': context.get('user_role'),
                    'context': context
                }
            )
            
            # Mettre à jour la session avec le dernier message
            session.last_activity = timezone.now()
            session.save(update_fields=['last_activity'])
            
            # Préparer les informations d'utilisation
            usage_info = response.get('usage', {})
            
            # Journaliser la réponse
            logger.info(f"Réponse générée pour la session {session_id} - Modèle: {CHATBOT_MODEL}, Tokens: {usage_info.get('total_tokens', 'inconnu')}")
            
            # Préparer la réponse
            response_data = {
                'session_id': str(session.session_id),
                'message_id': str(bot_message.id),
                'response': bot_message.content,
                'context': session.context,
                'session_type': session.session_type,
                'user_role': session.user_role,
                'timestamp': bot_message.sent_at.isoformat(),
                'model': CHATBOT_MODEL,
                'usage': usage_info,
                'status': 'success'
            }
            
            # Créer la réponse avec les en-têtes CORS
            response = Response(response_data)
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
            response['Access-Control-Allow-Credentials'] = 'true'
            
            logger.info(f"Réponse du chatbot envoyée pour la session {session.session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération ou de l'enregistrement de la réponse: {str(e)}", exc_info=True)
            error_response = Response(
                {
                    'error': f"Une erreur est survenue lors de la génération de la réponse: {str(e)}",
                    'status': 'error',
                    'session_id': str(session.session_id) if session else None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            error_response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
            error_response['Access-Control-Allow-Credentials'] = 'true'
            return error_response
            
    except Exception as e:
        error_msg = f"Erreur lors du traitement de la requête de chat: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return Response(
            {'error': 'Une erreur est survenue lors du traitement de votre demande', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _get_or_create_session(session_id, user, session_type='GENERAL'):
    """
    Récupère une session existante ou en crée une nouvelle si elle n'existe pas
    
    Args:
        session_id: ID de la session à récupérer (peut être None)
        user: Utilisateur associé à la session (peut être None pour les utilisateurs anonymes)
        session_type: Type de session ('GENERAL', 'MEDICAL', 'TECHNICAL', 'ADMIN')
        
    Returns:
        Instance de ChatSession existante ou nouvellement créée
        
    Raises:
        Exception: En cas d'erreur lors de la création ou de la récupération de la session
    """
    try:
        if session_id:
            try:
                session = ChatSession.objects.get(session_id=session_id)
                # Mettre à jour la date de dernière activité
                session.last_activity = timezone.now()
                
                # Mettre à jour le type de session et le rôle si nécessaire
                if session_type and session_type != session.session_type:
                    session.session_type = session_type
                    # Mettre à jour le contexte avec le nouveau type de session
                    if not session.context:
                        session.context = {}
                    session.context['session_type'] = session_type
                
                # Mettre à jour le rôle de l'utilisateur s'il est authentifié
                if user and user.is_authenticated:
                    user_role = user.role.name if hasattr(user, 'role') and user.role else 'USER'
                    if user_role != session.user_role:
                        session.user_role = user_role
                        if not session.context:
                            session.context = {}
                        session.context['user_role'] = user_role
                
                # Sauvegarder les modifications
                update_fields = ['last_activity']
                if hasattr(session, 'session_type'):
                    update_fields.append('session_type')
                if hasattr(session, 'user_role'):
                    update_fields.append('user_role')
                if hasattr(session, 'context'):
                    update_fields.append('context')
                
                session.save(update_fields=update_fields)
                logger.debug(f"Session existante mise à jour - ID: {session_id}, Type: {session.session_type}, Rôle: {session.user_role}")
                return session
                
            except ChatSession.DoesNotExist:
                logger.debug(f"Session non trouvée, création d'une nouvelle avec ID: {session_id}")
                pass
        
        # Déterminer le rôle de l'utilisateur
        user_role = None
        if user and user.is_authenticated:
            user_role = user.role.name if hasattr(user, 'role') and user.role else 'USER'
        
        # Créer une nouvelle session avec le type et le rôle appropriés
        new_session_id = session_id or str(uuid.uuid4())
        is_anonymous = user is None
        
        # Préparer le contexte de la session
        context = {
            'user_role': user_role,
            'session_type': session_type,
            'previous_questions': [],
            'medical_context': {}
        }
        
        # Créer la session
        session = ChatSession.objects.create(
            session_id=new_session_id,
            user=user,
            is_anonymous=is_anonymous,
            session_type=session_type,
            user_role=user_role,
            context=context,
            started_at=timezone.now(),
            last_activity=timezone.now()
        )
        
        logger.info(f"Nouvelle session créée - ID: {session.session_id}, Type: {session_type}, Rôle: {user_role or 'Anonyme'}")
        return session
        
    except Exception as e:
        logger.error(f"Erreur lors de la création d'une nouvelle session: {str(e)}", exc_info=True)
        raise

def _get_chat_history(session, limit=10):
    """
    Récupère l'historique des messages d'une session
    
    Args:
        session: Instance de ChatSession
        limit: Nombre maximum de messages à récupérer (par défaut: 10)
        
    Returns:
        QuerySet des messages triés par date de création (du plus ancien au plus récent)
    """
    if not session or not hasattr(session, 'id'):
        return []
        
    try:
        # Récupérer les messages les plus récents
        messages = ChatMessage.objects.filter(
            session=session
        ).order_by('-sent_at')[:limit]
        
        # Convertir en liste et inverser l'ordre pour avoir du plus ancien au plus récent
        return list(reversed(messages))
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique des messages: {str(e)}")
        return []


class ChatSessionCreateView(APIView):
    """
    Vue pour créer une nouvelle session de chat.
    Accessible sans authentification pour permettre aux utilisateurs anonymes de démarrer une session.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Préparer les données avec le type de session par défaut si non fourni
        data = request.data.copy()
        if 'session_type' not in data:
            data['session_type'] = 'GENERAL'
            
        # Déterminer si l'utilisateur est authentifié
        user = request.user if request.user.is_authenticated else None
        
        # Si l'utilisateur est authentifié, utiliser son rôle, sinon définir un rôle par défaut
        if user:
            data['user_role'] = user.role if hasattr(user, 'role') else 'USER'
        else:
            data['is_anonymous'] = True
            data['user_role'] = 'ANONYMOUS'
        
        serializer = ChatSessionCreateSerializer(
            data=data,
            context={'request': request, 'user': user}
        )
        
        if serializer.is_valid():
            try:
                session = serializer.save()
                
                # Préparer la réponse avec les informations de session
                response_data = {
                    'session_id': str(session.session_id),
                    'is_anonymous': session.is_anonymous,
                    'session_type': session.session_type,
                    'user_role': session.user_role,
                    'started_at': session.started_at.isoformat(),
                    'context': session.context,
                    'status': 'success',
                    'message': 'Session créée avec succès'
                }
                
                # Créer la réponse avec les en-têtes CORS
                response = Response(response_data)
                # Ajouter les en-têtes CORS nécessaires
                response = Response(response_data, status=status.HTTP_201_CREATED)
                response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
                response['Access-Control-Allow-Credentials'] = 'true'
                return response
                
            except Exception as e:
                logger.error(f"Erreur lors de la création de la session: {str(e)}", exc_info=True)
                return Response(
                    {'error': str(e), 'status': 'error'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        logger.warning(f"Erreur de validation lors de la création de session: {serializer.errors}")
        return Response(
            {'errors': serializer.errors, 'status': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_feedback(request):
    try:
        message_id = request.data.get('message_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not message_id or not rating:
            return Response(
                {'error': 'message_id et rating sont obligatoires'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            message = ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            return Response(
                {'error': 'Message non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        feedback = ChatFeedback.objects.create(
            message=message,
            rating=rating,
            comment=comment
        )
        
        # Mettre à jour la note moyenne du message
        message.average_rating = message.feedback.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        message.save()
        
        return Response({
            'success': True,
            'feedback_id': feedback.id,
            'average_rating': message.average_rating
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la soumission du feedback: {str(e)}")
        return Response(
            {'error': 'Une erreur est survenue lors de la soumission du feedback'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )