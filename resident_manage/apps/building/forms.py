from django.forms import ModelForm
from django import forms
from resident_manage.apps.building.models import Building, Room
from django.core.exceptions import ValidationError


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = [
            'building_id', 
            'name', 
            'address', 
            'total_floors', 
            'total_rooms', 
            'total_availble_rooms', 
            'status'
        ]
        
        # Mapping các input field của Django với class CSS trong file HTML của bạn
        widgets = {
            'building_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập mã tòa nhà (VD: B01)',
                'autofocus': 'autofocus' # Tự động focus khi vào trang
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tên tòa nhà'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Nhập địa chỉ chi tiết',
                'style': 'resize: vertical;' # Cho phép kéo giãn chiều dọc
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'placeholder': '0'
            }),
            'total_rooms': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'placeholder': '0'
            }),
            'total_availble_rooms': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'placeholder': '0'
            }),
            # Select box cho trạng thái
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    # (Optional) Hàm clean để validate logic riêng nếu cần
    def clean_building_id(self):
        building_id = self.cleaned_data.get('building_id')
        # Kiểm tra trùng lặp (dù unique=True đã check, nhưng check ở đây để custom lỗi)
        if Building.objects.filter(building_id=building_id).exists() and not self.instance.pk:
            raise forms.ValidationError("Mã tòa nhà này đã tồn tại.")
        return building_id
        
class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        # Những trường cần nhập khi tạo mới
        fields = [
            'room_id', 
            'building', 
            'room_number', 
            'floor_number', 
            'room_area', 
            'rent_price', 
            'type_listing', 
            'status'
            # Lưu ý: Mình tạm ẩn 'owner' và 'room_residents' lúc tạo mới 
            # vì thường tạo phòng xong mới gán người vào sau. 
            # Nếu bạn muốn gán luôn thì thêm vào list này.
        ]
        
        widgets = {
            'room_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập mã định danh (VD: R-A-101)',
                'autofocus': 'autofocus'
            }),
            'building': forms.Select(attrs={
                'class': 'form-select'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Số phòng (VD: 101, 205B)'
            }),
            'floor_number': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'placeholder': 'Nhập số tầng'
            }),
            'room_area': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01', # Cho phép nhập số lẻ
                'placeholder': 'Diện tích (m²)'
            }),
            'rent_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '1000',
                'placeholder': 'Nhập giá (VNĐ)'
            }),
            'type_listing': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    # 1. Validate Mã phòng (Unique globally)
    def clean_room_id(self):
        room_id = self.cleaned_data.get('room_id')
        if Room.objects.filter(room_id=room_id).exists():
            raise ValidationError("Mã căn hộ này đã tồn tại trên hệ thống.")
        return room_id
    
    def __init__(self, *args, **kwargs):
        super(RoomCreateForm, self).__init__(*args, **kwargs)
        
        # Nếu có dữ liệu initial 'building', khóa field đó lại
        if self.initial.get('building'):
            self.fields['building'].disabled = True
            self.fields['building'].widget.attrs['style'] = 'background-color: #e9ecef; cursor: not-allowed;'

    # 2. Validate logic: Một tòa nhà không được có 2 phòng trùng số (VD: 2 phòng 101)
    def clean(self):
        cleaned_data = super().clean()
        building = cleaned_data.get('building')
        room_number = cleaned_data.get('room_number')

        if building and room_number:
            # Kiểm tra xem trong tòa nhà này đã có số phòng này chưa
            if Room.objects.filter(building=building, room_number=room_number).exists():
                # Gán lỗi vào trường room_number
                self.add_error('room_number', f"Phòng số {room_number} đã tồn tại trong tòa nhà {building.name}.")
        
        return cleaned_data
    
class BuildingUpdateForm(ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'total_floors', 'status']
        

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['building', 'room_number', 'status', 'owner']


class RoomUpdateForm(ModelForm):
    class Meta:
        model = Room
        fields = ['status', 'owner', 'room_residents']