from django.contrib import admin
from resident_manage.apps.building.models import Building, Room
from .models import Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['citizen_id', 'full_name', 'date_of_birth', 'gender', 'phone_number', 'email', 'building', 'room', 'created_at']
    list_filter = ['gender', 'building', 'created_at']
    search_fields = ['citizen_id', 'first_name', 'last_name', 'phone_number', 'email']
    ordering = ['-created_at']
    autocomplete_fields = ['building', 'room']
    
    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"
    full_name.short_description = 'Họ và tên'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'room':
            building_id = request.GET.get('building')
            if building_id:
                kwargs['queryset'] = Room.objects.filter(building_id=building_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)