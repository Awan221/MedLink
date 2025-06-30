from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import BloodDonationCenter, BloodInventory, BloodDonation

class BloodInventoryInline(admin.TabularInline):
    model = BloodInventory
    extra = 1
    readonly_fields = ('status', 'last_updated')
    fields = ('blood_type', 'quantity_ml', 'minimum_required_ml', 'status', 'last_updated')

class BloodDonationInline(admin.TabularInline):
    model = BloodDonation
    extra = 0
    readonly_fields = ('donation_link', 'created_at')
    fields = ('donation_link', 'donor_name', 'donor_blood_type', 'quantity_ml', 'is_processed', 'donation_date', 'created_at')
    
    def donation_link(self, obj):
        url = reverse('admin:bloodbank_blooddonation_change', args=[obj.id])
        return format_html('<a href="{}">Voir le don #{}</a>', url, obj.id)
    donation_link.short_description = 'Lien vers le don'
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(BloodDonationCenter)
class BloodDonationCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'phone', 'is_active', 'inventory_summary')
    list_filter = ('is_active', 'region', 'city')
    search_fields = ('name', 'address', 'city', 'region')
    list_editable = ('is_active',)
    inlines = [BloodInventoryInline, BloodDonationInline]
    readonly_fields = ('created_at', 'updated_at', 'location_map')
    fieldsets = (
        (None, {
            'fields': ('name', 'is_active')
        }),
        ('Coordonnées', {
            'fields': ('address', 'city', 'region', 'country', 'phone', 'email')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude', 'location_map')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def inventory_summary(self, obj):
        inventories = obj.inventory.all()
        if not inventories.exists():
            return "Aucun inventaire"
            
        status_icons = {
            'critical': '🟥',  # Rouge
            'low': '🟨',       # Jaune
            'warning': '🟧',    # Orange
            'good': '🟩'        # Vert
        }
        
        items = []
        for inv in inventories.order_by('blood_type'):
            status = inv.status
            icon = status_icons.get(status, '⚪')
            items.append(f"{inv.blood_type}: {inv.quantity_ml}ml {icon}")
            
        return mark_safe(" | ".join(items))
    inventory_summary.short_description = "Inventaire"
    
    def location_map(self, instance):
        if instance.latitude and instance.longitude:
            return mark_safe(
                f'<div id="map" style="height: 300px; width: 100%;"></div>'
                f'<script>'
                f'function initMap() {{'
                f'  const center = {{lat: {instance.latitude}, lng: {instance.longitude}}};'
                f'  const map = new google.maps.Map(document.getElementById("map"), {{'
                f'    zoom: 15,'
                f'    center: center,'
                f'  }});'
                f'  new google.maps.Marker({{position: center, map: map, title: "{instance.name}"}});'
                f'}}'
                f'</script>'
                f'<script async defer '
                f'src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">'
                f'</script>'
            )
        return "Coordonnées GPS non disponibles"
    location_map.allow_tags = True
    location_map.short_description = "Carte"

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_type', 'center_name', 'quantity_ml', 'minimum_required_ml', 'status_badge', 'last_updated')
    list_filter = ('blood_type', 'center__city', 'last_updated')
    search_fields = ('center__name', 'blood_type')
    readonly_fields = ('status', 'last_updated')
    list_editable = ('quantity_ml', 'minimum_required_ml')
    
    def center_name(self, obj):
        return obj.center.name
    center_name.short_description = 'Centre de don'
    center_name.admin_order_field = 'center__name'
    
    def status_badge(self, obj):
        status_classes = {
            'critical': 'error',
            'low': 'warning',
            'warning': 'warning',
            'good': 'success'
        }
        status_text = dict(BloodInventory.STATUS_CHOICES).get(obj.status, obj.status)
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            status_classes.get(obj.status, 'secondary'),
            status_text
        )
    status_badge.short_description = 'Statut'
    status_badge.admin_order_field = 'status'

@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor_name', 'donor_blood_type', 'donation_center_name', 
                   'donation_date', 'quantity_ml', 'is_processed_badge', 'created_at')
    list_filter = ('is_processed', 'donation_date', 'donor_blood_type', 'donation_center__city')
    search_fields = ('donor_name', 'donation_center__name', 'donor_phone')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'donation_date'
    list_select_related = ('donation_center', 'created_by')
    
    fieldsets = (
        (None, {
            'fields': ('donor_name', 'donor_blood_type', 'donor_phone')
        }),
        ('Détails du don', {
            'fields': ('donation_center', 'donation_date', 'quantity_ml', 'is_processed', 'notes')
        }),
        ('Traçabilité', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def donation_center_name(self, obj):
        return obj.donation_center.name
    donation_center_name.short_description = 'Centre de don'
    donation_center_name.admin_order_field = 'donation_center__name'
    
    def is_processed_badge(self, obj):
        if obj.is_processed:
            return format_html('<span class="badge badge-success">Traité</span>')
        return format_html('<span class="badge badge-warning">En attente</span>')
    is_processed_badge.short_description = 'Statut'
    is_processed_badge.admin_order_field = 'is_processed'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
        # Mettre à jour l'inventaire si le don est marqué comme traité
        if obj.is_processed and 'is_processed' in form.changed_data:
            obj._update_inventory()
    
    def get_readonly_fields(self, request, obj=None):
        # Permettre la modification de is_processed uniquement si l'utilisateur a les droits
        if request.user.is_superuser or request.user.groups.filter(name='Gestionnaire Banque de Sang').exists():
            return self.readonly_fields
        return self.readonly_fields + ('is_processed',)
