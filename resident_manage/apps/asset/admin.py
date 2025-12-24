from django.contrib import admin
from resident_manage.apps.building.models import Room, Building
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=['asset_id','name','building','room','date_maintained','status','detail_address']
    list_filter=['building','room','status','created_at']
    search_fields=['asset_id','asset_name','detail_address']
    ordering=['-created_at']
    autocomplete_fields=['building','room']
    
    def name(self,obj):
        return obj.asset_name
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'room':
            building_id = request.GET.get('building')
            if building_id:
                kwargs['queryset'] = Room.objects.filter(building_id=building_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)