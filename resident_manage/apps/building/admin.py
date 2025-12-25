from django.contrib import admin
from .models import Building, Room


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['building_id', 'name', 'address', 'total_floors', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['building_id', 'name', 'address']
    ordering = ['building_id']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'building', 'floor_number', 'room_number', 'status', 'type_listing', 'created_at', 'room_area']
    list_filter = ['status', 'type_listing', 'building', 'floor_number']
    search_fields = ['room_id', 'room_number']
    ordering = ['building', 'floor_number', 'room_number']
    autocomplete_fields = ['building']

