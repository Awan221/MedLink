from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (
    CurrentUserView, RegisterView, LoginView, LogoutView,
    RolePermissionListView, RolePermissionDetailView,
    SubRolePermissionListView, SubRolePermissionDetailView,
    PermissionCheckView, UserListView, UserDetailView,
    PendingRegistrationRequestsView, ProcessRegistrationRequestView,
    ManageRolesView, RoleListView, UserRegistrationRequestView,
    ValidateRegistrationRequestView
)
from .views_password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .views_admin_registration import UserRegistrationRequestStatsView
from .views_admin_dashboard import AdminRecentActivityView, AdminAlertsView

urlpatterns = [
    path('admin/stats/', UserRegistrationRequestStatsView.as_view(), name='admin-stats'),
    path('admin/recent-activity/', AdminRecentActivityView.as_view(), name='admin-recent-activity'),
    path('admin/alerts/', AdminAlertsView.as_view(), name='admin-alerts'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('register/', UserRegistrationRequestView.as_view(), name='register'),
    path('register/validate/<int:pk>/', ValidateRegistrationRequestView.as_view(), name='validate-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Gestion des permissions
    path('permissions/', RolePermissionListView.as_view(), name='permission-list'),
    path('permissions/<int:pk>/', RolePermissionDetailView.as_view(), name='permission-detail'),
    path('sub-permissions/', SubRolePermissionListView.as_view(), name='sub-permission-list'),
    path('sub-permissions/<int:pk>/', SubRolePermissionDetailView.as_view(), name='sub-permission-detail'),
    path('check-permission/', PermissionCheckView.as_view(), name='check-permission'),
    
    # Gestion des utilisateurs
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/roles/', ManageRolesView.as_view(), name='manage-roles'),
    
    # Gestion des demandes d'inscription
    path('registration-requests/pending/', PendingRegistrationRequestsView.as_view(), name='pending-registration-requests'),
    path('registration-requests/<int:pk>/process/', ProcessRegistrationRequestView.as_view(), name='process-registration-request'),
    
    # Gestion des rôles
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/manage/', ManageRolesView.as_view(), name='manage-roles'),
    
    # Réinitialisation de mot de passe
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]