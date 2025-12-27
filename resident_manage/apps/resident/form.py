from django import forms
from django.db.models import Q
from .models import Resident
from resident_manage.apps.building.models import Building, Room


class ResidentForm(forms.ModelForm):
    
    class Meta:
        model = Resident
        fields = [
            'citizen_id', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'phone_number', 'email', 'address',
            'relationship', 'building', 'room'
        ]
        widgets = {
            'citizen_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: 0123456789'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0987654321'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ'
            }),
            'relationship': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        building_id = kwargs.pop('building_id', None)
        room_id = kwargs.pop('room_id', None)
        super().__init__(*args, **kwargs)
        
        # Nếu chỉnh sửa, cho phép chọn phòng hiện tại hoặc phòng có sẵn
        if self.instance and self.instance.pk:
            self.fields['room'].queryset = Room.objects.filter(
                Q(id=self.instance.room_id) | Q(status='available')
            )
            if self.instance.room:
                self.fields['building'].initial = self.instance.room.building
        # Nếu tạo từ phòng cụ thể
        elif room_id:
            try:
                room = Room.objects.get(id=room_id)
                self.fields['room'].initial = room
                self.fields['room'].queryset = Room.objects.filter(
                    Q(id=room_id) | Q(status='available')
                )
                self.fields['building'].initial = room.building
            except Room.DoesNotExist:
                self.fields['room'].queryset = Room.objects.filter(status='available')
        # Nếu tạo từ tòa nhà cụ thể
        elif building_id:
            try:
                building = Building.objects.get(id=building_id)
                self.fields['building'].initial = building
                self.fields['room'].queryset = Room.objects.filter(
                    building=building, status='available'
                )
            except Building.DoesNotExist:
                self.fields['room'].queryset = Room.objects.filter(status='available')
        else:
            self.fields['room'].queryset = Room.objects.filter(status='available')

    def clean(self):
        cleaned_data = super().clean()
        citizen_id = cleaned_data.get('citizen_id')
        
        # Kiểm tra CMND/CCCD không trùng
        if self.instance and self.instance.pk:
            # Nếu là chỉnh sửa, kiểm tra CMND/CCCD không trùng với resident khác
            if Resident.objects.filter(citizen_id=citizen_id).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Số CMND/CCCD này đã tồn tại.")
        else:
            # Nếu là tạo mới
            if Resident.objects.filter(citizen_id=citizen_id).exists():
                raise forms.ValidationError("Số CMND/CCCD này đã tồn tại.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=True)
        return instance
