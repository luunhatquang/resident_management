from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source='resident.last_name', read_only=True)
    contract_code = serializers.CharField(source='contract.contract_id', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'