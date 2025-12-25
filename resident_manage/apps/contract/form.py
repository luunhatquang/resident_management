from django import forms
from django.db.models import Q 
from .models import Contract
from resident_manage.apps.resident.models import Resident
from resident_manage.apps.building.models import Room
from datetime import timedelta
from django.utils import timezone

class ContractForm(forms.ModelForm):
    
    class Meta:
        model = Contract
        fields = [
            'contract_id', 'contract_type',
            'resident', 'room',
            'start_date', 'end_date', 'sign_date',
            'total_price', 'price_per_month', 'deposit'
        ]
        widgets = {
            'contract_id': forms.TextInput(attrs={'class': 'form-control','placeholder': "VD: HD-2025-011"}),
            'contract_type': forms.Select(attrs={'class': 'form-control'}),
            'resident': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sign_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control','placeholder': "Tổng giá trị hợp đồng", 'step': "0.01"}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control','placeholder': "Giá thuê/tháng", 'step': "0.01"}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control','placeholder': "Tiền cọc", 'step': "0.01"}),
        }
        
    def __init__(self, *args, **kwargs):
        resident_id = kwargs.pop('resident_id', None)
        room_id = kwargs.pop('room_id', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['room'].queryset = Room.objects.filter(
                Q(id=self.instance.room_id) | Q(status='available')
            )
        elif resident_id:
            try:
                resident = Resident.objects.get(id=resident_id)
                if resident.room:
                    self.fields['room'].queryset = Room.objects.filter(
                        Q(id=resident.room_id) | Q(status='available')
                    ).distinct()
                    self.fields['room'].initial = resident.room
                else:
                    self.fields['room'].queryset = Room.objects.filter(status='available')
                self.fields['resident'].initial = resident
            except Resident.DoesNotExist:
                self.fields['room'].queryset = Room.objects.filter(status='available')
        elif room_id:
            try:
                room = Room.objects.get(id=room_id)
                self.fields['room'].initial = room
                self.fields['room'].queryset = Room.objects.filter(
                    Q(id=room_id) | Q(status='available')
                )
                res = Resident.objects.filter(room=room).first()
                if res:
                    self.fields['resident'].initial = res
            except Room.DoesNotExist:
                self.fields['room'].queryset = Room.objects.filter(status='available')
        else:
            self.fields['room'].queryset = Room.objects.all()
        
        
                    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Ngày bắt đầu phải nhỏ hơn ngày kết thúc.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        today = timezone.now().date()
        
        if instance.end_date:
            if instance.end_date < today:
                instance.status = 'expired'
            elif (instance.end_date - today) <= timedelta(days=30):
                instance.status = 'will_expire'
            elif instance.start_date and instance.start_date <= today:
                instance.status = 'active'
            else:
                instance.status = 'pending'
        else:
            instance.status = 'pending'
        
        if commit:
            instance.save()
        return instance
