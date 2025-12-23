from django.contrib import admin
from .models import Notification
from resident_management.apps.building.models import Room


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'priority', 'resident', 'building', 'room', 'is_read', 'send_at', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'resident__first_name', 'resident__last_name', 'room__room_id']       
    ordering = ['-created_at']
    autocomplete_fields = ['resident', 'building', 'room', 'contract']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter room theo building đã chọn
        if db_field.name == 'room':
            building_id = request.GET.get('building')
            if building_id:
                kwargs['queryset'] = Room.objects.filter(building_id=building_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    