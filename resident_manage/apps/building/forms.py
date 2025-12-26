from django.forms import ModelForm
from resident_manage.apps.building.models import Building, Room


class BuildingCreateForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'
        
class RoomCreateForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['room_residents', 'owner']
    
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