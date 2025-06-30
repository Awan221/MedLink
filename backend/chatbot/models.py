from django.db import models
from django.utils import timezone
from authentication.models import User

class ChatbotKnowledgeBase(models.Model):
    CATEGORY_CHOICES = (
        ('DISEASE', 'Maladie'),
        ('SYMPTOM', 'Symptôme'),
        ('MEDICATION', 'Médicament'),
        ('PROCEDURE', 'Procédure médicale'),
        ('FIRST_AID', 'Premiers secours'),
        ('NUTRITION', 'Nutrition'),
        ('PREVENTION', 'Prévention'),
        ('GENERAL', 'Information générale'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    keywords = models.TextField(help_text="Mots-clés séparés par des virgules")
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_knowledge')
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    class Meta:
        verbose_name = 'Base de connaissance du chatbot'
        verbose_name_plural = 'Base de connaissances du chatbot'
        ordering = ['category', 'title']

class ChatSession(models.Model):
    SESSION_TYPES = (
        ('GENERAL', 'Général'),
        ('MEDICAL', 'Médical'),
        ('TECHNICAL', 'Technique'),
        ('ADMIN', 'Administratif'),
    )
    
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')
    is_anonymous = models.BooleanField(default=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='GENERAL')
    user_role = models.CharField(max_length=50, blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    context = models.JSONField(default=dict, blank=True)  # Pour stocker le contexte de la session
    
    def __str__(self):
        return f"Session {self.session_id} - {'Anonyme' if self.is_anonymous else self.user.email}"
    
    class Meta:
        verbose_name = 'Session de chat'
        verbose_name_plural = 'Sessions de chat'
        ordering = ['-last_activity']

class ChatMessage(models.Model):
    TYPE_CHOICES = (
        ('USER', 'Utilisateur'),
        ('BOT', 'Chatbot'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    # Pour les messages bot uniquement
    knowledge_base_reference = models.ForeignKey(ChatbotKnowledgeBase, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Pour stocker les métadonnées du message
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}..."
    
    class Meta:
        verbose_name = 'Message de chat'
        verbose_name_plural = 'Messages de chat'
        ordering = ['sent_at']

class ChatFeedback(models.Model):
    RATING_CHOICES = (
        (1, '1 - Très insatisfait'),
        (2, '2 - Insatisfait'),
        (3, '3 - Neutre'),
        (4, '4 - Satisfait'),
        (5, '5 - Très satisfait'),
    )
    
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback sur message {self.message.id} - Note: {self.rating}"
    
    class Meta:
        verbose_name = 'Feedback de chat'
        verbose_name_plural = 'Feedbacks de chat'
        ordering = ['-created_at']