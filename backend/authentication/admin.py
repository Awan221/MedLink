from django.contrib import admin
from .models import Permission, Role, UserRegistrationRequest, User, RolePermission, SubRolePermission

@admin.register(UserRegistrationRequest)
class UserRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'status', 'created_at')
    list_filter = ('status', 'role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for registration_request in queryset:
            if registration_request.status == 'PENDING':
                registration_request.status = 'APPROVED'
                registration_request.save()
                # Créer l'utilisateur
                User.objects.create_user(
                    email=registration_request.email,
                    password=registration_request.password,
                    first_name=registration_request.first_name,
                    last_name=registration_request.last_name,
                    role=registration_request.role,
                    status='ACTIF'
                )
    approve_requests.short_description = "Approuver les demandes sélectionnées"

    def reject_requests(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_requests.short_description = "Rejeter les demandes sélectionnées"

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(RolePermission)
admin.site.register(SubRolePermission)
