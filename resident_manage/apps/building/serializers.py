# resident_manage/apps/building/serializers.py
from rest_framework import serializers
from .models import Building, Room

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'  # Lấy tất cả các trường
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  # Lấy tất cả các trường