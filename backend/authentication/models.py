from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')

class Role(Group):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(_('adresse email'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=30)
    last_name = models.CharField(_('nom'), max_length=30)
    phone = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    specialist_type = models.ForeignKey('SpecialistType', null=True, blank=True, on_delete=models.SET_NULL, related_name='specialists')
    hopital = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=100, blank=True)
    numero_licence = models.CharField(max_length=20, blank=True)
    date_licence = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(_('actif'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    date_joined = models.DateTimeField(_('date d\'inscription'), default=timezone.now)
    last_login = models.DateTimeField(_('dernière connexion'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class UserRegistrationRequest(models.Model):
    STATUS_CHOICES = [
            ('pending', 'En attente'),
            ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    hopital = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    numero_licence = models.CharField(max_length=20, unique=True)
    date_licence = models.DateField()
    documents = models.FileField(upload_to='registration_documents/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('registration request')
        verbose_name_plural = _('registration requests')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = _('permission de rôle')
        verbose_name_plural = _('permissions de rôle')
    
    def __str__(self):
        return f'{self.role} - {self.permission}'

class SubRolePermission(models.Model):
    class SubRole(models.TextChoices):
        GENERAL_PRACTITIONER = 'GENERAL_PRACTITIONER', _('Médecin Généraliste')
        CARDIOLOGIST = 'CARDIOLOGIST', _('Cardiologue')
        DIABETOLOGIST = 'DIABETOLOGIST', _('Diabétologue')
        NEUROLOGIST = 'NEUROLOGIST', _('Neurologue')
        PEDIATRICIAN = 'PEDIATRICIAN', _('Pédiatre')
        RADIOLOGIST = 'RADIOLOGIST', _('Radiologue')
        IMAGING_TECHNICIAN = 'IMAGING_TECHNICIAN', _('Technicien en Imagerie')
        LAB_TECHNICIAN = 'LAB_TECHNICIAN', _('Technicien de Laboratoire')

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='subrole_permissions')
    sub_role = models.CharField(max_length=30, choices=SubRole.choices)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='subrole_permissions')
    is_allowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('role', 'sub_role', 'permission')
        ordering = ['role', 'sub_role', 'permission']

    def __str__(self):
        return f"{self.role} - {self.sub_role} - {self.permission}"

class UserDocument(models.Model):
    DOCUMENT_TYPES = (
        ('REGISTRATION', 'Document d\'inscription'),
        ('LICENSE', 'Licence professionnelle'),
        ('IDENTITY', 'Pièce d\'identité'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='user_documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"

class SpecialistType(models.Model):
    CARDIOLOGIST = 'cardiologist'
    NEUROLOGIST = 'neurologist'
    PEDIATRICIAN = 'pediatrician'
    GYNECOLOGIST = 'gynecologist'
    DERMATOLOGIST = 'dermatologist'
    ORTHOPEDIST = 'orthopedist'
    OPHTHALMOLOGIST = 'ophthalmologist'
    OTHER = 'other'

    SPECIALIST_CHOICES = [
        (CARDIOLOGIST, 'Cardiologue'),
        (NEUROLOGIST, 'Neurologue'),
        (PEDIATRICIAN, 'Pédiatre'),
        (GYNECOLOGIST, 'Gynécologue'),
        (DERMATOLOGIST, 'Dermatologue'),
        (ORTHOPEDIST, 'Orthopédiste'),
        (OPHTHALMOLOGIST, 'Ophtalmologue'),
        (OTHER, 'Autre Spécialité'),
    ]

    name = models.CharField(max_length=50, choices=SPECIALIST_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _('type de spécialiste')
        verbose_name_plural = _('types de spécialistes')