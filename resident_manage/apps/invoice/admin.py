from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'room', 'contract', 'service', 'count_unit', 'unit_price', 'total_price', 'status', 'start_date', 'date', 'end_date', 'created_at']
    list_filter = ['service', 'status', 'start_date', 'end_date']
    search_fields = ['invoice_id', 'room__room_id', 'room__room_number', 'contract__contract_id']
    ordering = ['-created_at']
    autocomplete_fields = ['room', 'contract']
    
