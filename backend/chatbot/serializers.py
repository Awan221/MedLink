import uuid
from rest_framework import serializers
from .models import ChatbotKnowledgeBase, ChatSession, ChatMessage, ChatFeedback

class ChatbotKnowledgeBaseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ChatbotKnowledgeBase
        fields = ['id', 'title', 'content', 'category', 'keywords', 
                 'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'message_type', 'content', 
                 'sent_at', 'knowledge_base_reference']
        read_only_fields = ['id', 'sent_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'user', 'is_anonymous', 
                 'started_at', 'last_activity', 'messages']
        read_only_fields = ['id', 'started_at', 'last_activity']

class ChatFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFeedback
        fields = ['id', 'message', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatSessionCreateSerializer(serializers.ModelSerializer):
    session_type = serializers.ChoiceField(
        choices=ChatSession.SESSION_TYPES,
        default='GENERAL',
        required=False
    )
    
    class Meta:
        model = ChatSession
        fields = ['session_type']  # Champ optionnel pour le type de session
        read_only_fields = ['session_id', 'user', 'is_anonymous', 'started_at', 'last_activity', 'user_role', 'context']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        session_type = validated_data.pop('session_type', 'GENERAL')
        
        # Préparer le contexte initial
        context = {
            'previous_questions': [],
            'medical_context': {},
            'session_type': session_type,
            'user_role': user.role.name if user and hasattr(user, 'role') and user.role else None
        }
        
        # Créer la session avec le type et le contexte
        session = ChatSession.objects.create(
            session_id=str(uuid.uuid4()),
            user=user,
            is_anonymous=user is None,
            session_type=session_type,
            user_role=context['user_role'],
            context=context
        )
        return session

class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    message = serializers.CharField()
    user_id = serializers.IntegerField(required=False, allow_null=True)