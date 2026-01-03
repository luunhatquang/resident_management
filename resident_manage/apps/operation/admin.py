from django.contrib import admin
from .models import OperationExpense

@admin.register(OperationExpense)
class OperationExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_id', 'expense_title', 'category_type', 'building', 'date', 'count', 'amount', 'total_amount', 'status', 'recorded_by']
    list_filter = ['category_type', 'building', 'status', 'date']
    search_fields = ['expense_id', 'expense_title', 'building__name', 'recorded_by__username']
    ordering = ['-date', '-created_at']
    readonly_fields = ['total_amount']
    autocomplete_fields = ['building', 'recorded_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.recorded_by:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)
