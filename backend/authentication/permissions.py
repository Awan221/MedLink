from rest_framework import permissions
from rest_framework.permissions import IsAdminUser as BaseIsAdminUser
from imaging.models import ActionLog

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name in ['admin', 'SUPER_ADMIN']
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'SUPER_ADMIN'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed


class IsInfirmier(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que les utilisateurs avec le rôle 'infirmier'.
    """
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'INFIRMIER'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed


class IsAdminUser(BaseIsAdminUser):
    """
    Surcharge de la permission IsAdminUser de DRF pour inclure la journalisation.
    """
    def has_permission(self, request, view):
        allowed = super().has_permission(request, view)
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (is_staff: {getattr(request.user, 'is_staff', False)})"
            )
        return allowed

class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'doctor'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed

class IsSpecialiste(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'specialist'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed

class IsRadiologue(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'radiologist'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed

class IsTechnicien(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'lab_technician'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed

class IsBanqueSang(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role and request.user.role.name == 'blood_bank_manager'
        if not allowed and request.user.is_authenticated:
            ActionLog.objects.create(
                user=request.user,
                action='ACCESS_DENIED',
                target_type=view.__class__.__name__,
                target_id='',
                status='FAIL',
                message=f"Tentative d'accès refusée à {view.__class__.__name__} (role: {getattr(request.user.role, 'name', None) if request.user.role else None})"
            )
        return allowed