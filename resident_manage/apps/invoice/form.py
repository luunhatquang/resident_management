from django import forms
from .models import Invoice
from resident_manage.apps.building.models import Room
from resident_manage.apps.resident.models import Resident
from resident_manage.apps.contract.models import Contract

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_id', 'invoice_title', 'service', 'contract', 'room', 'resident',
            'date', 'count_unit', 'unit_price', 'total_price', 'status',
            'start_date', 'end_date',
        ]
        widgets = {
            'invoice_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã hóa đơn'}),
            'invoice_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nội dung hóa đơn'}),
            'service': forms.Select(attrs={'class': 'form-control', 'id': 'id_service'}),
            'contract': forms.Select(attrs={'class': 'form-control', 'id': 'id_contract'}),
            'room': forms.Select(attrs={'class': 'form-control', 'id': 'id_room'}),
            'resident': forms.Select(attrs={'class': 'form-control', 'id': 'id_resident'}),
            'count_unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_count_unit', 'placeholder': 'Số lượng đơn vị'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_unit_price', 'placeholder': 'Đơn giá'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_total_price', 'placeholder': 'Tổng tiền', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contract.objects.filter(
            contract_type='rent',
            status__in=['active', 'will_expire']
        )
        self.fields['contract'].required = False


class InvoiceUpdateForm(forms.ModelForm):
    """Form for updating existing invoices - only editable fields"""
    class Meta:
        model = Invoice
        fields = [
            'service', 'status', 'count_unit', 'unit_price', 'total_price',
            'start_date', 'end_date', 'date',
        ]
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control', 'id': 'id_service'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'count_unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_count_unit'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_unit_price'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_total_price', 'readonly': 'readonly'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
