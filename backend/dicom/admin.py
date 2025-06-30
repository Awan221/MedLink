from django.contrib import admin
from .models import DICOMStudy, DICOMSeries, DICOMInstance

class DICOMInstanceInline(admin.TabularInline):
    model = DICOMInstance
    extra = 0
    readonly_fields = ('sop_instance_uid', 'instance_number', 'file_path', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class DICOMSeriesInline(admin.TabularInline):
    model = DICOMSeries
    extra = 0
    readonly_fields = ('series_uid', 'series_number', 'modality', 'created_at')
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(DICOMStudy)
class DICOMStudyAdmin(admin.ModelAdmin):
    list_display = ('study_uid', 'patient', 'study_date', 'modality', 'created_at')
    list_filter = ('modality', 'created_at')
    search_fields = ('study_uid', 'patient__first_name', 'patient__last_name', 'study_description')
    readonly_fields = ('study_uid', 'created_at', 'updated_at')
    date_hierarchy = 'study_date'
    inlines = [DICOMSeriesInline]

@admin.register(DICOMSeries)
class DICOMSeriesAdmin(admin.ModelAdmin):
    list_display = ('series_uid', 'study', 'modality', 'series_number', 'created_at')
    list_filter = ('modality', 'created_at')
    search_fields = ('series_uid', 'study__study_uid', 'series_description')
    readonly_fields = ('series_uid', 'created_at')
    inlines = [DICOMInstanceInline]

@admin.register(DICOMInstance)
class DICOMInstanceAdmin(admin.ModelAdmin):
    list_display = ('sop_instance_uid', 'series', 'instance_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sop_instance_uid', 'series__series_uid')
    readonly_fields = ('sop_instance_uid', 'instance_number', 'file_path', 'created_at')
    
    def has_add_permission(self, request):
        return False
