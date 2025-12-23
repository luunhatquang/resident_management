from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_id', 'contract_type', 'resident', 'room', 'start_date', 'end_date', 'status', 'sign_date']
    list_filter = ['contract_type', 'status', 'sign_date', 'start_date', 'end_date']
    search_fields = ['contract_id', 'resident__first_name', 'resident__last_name', 'room__room_id']
    ordering = ['-sign_date']
    autocomplete_fields = ['resident', 'room']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('contract_id', 'contract_type', 'status')
        }),
        ('Liên kết', {
            'fields': ('resident', 'room')
        }),
        ('Thời gian', {
            'fields': ('sign_date', 'start_date', 'end_date')
        }),
        ('Tài chính', {
            'fields': ('total_price', 'price_per_month', 'deposit')
        }),
    )
    

