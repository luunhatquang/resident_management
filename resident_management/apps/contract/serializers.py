from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Contract
from resident_management.apps.building.models import Room


class ContractSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source='resident.full_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'contract_id', 'contract_type',
            'start_date', 'end_date', 'sign_date',
            'resident', 'resident_name',
            'room', 'room_number', 'building_name',
            'total_price', 'price_per_month', 'deposit',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['contract_id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validate logic nghiệp vụ:
        Một căn hộ (Room) không thể có 2 hợp đồng đang 'active' cùng lúc.
        """
        room = data.get('room')
        status = data.get('status', 'pending')

        # Nếu đang tạo mới hoặc cập nhật trạng thái thành active
        if status == 'active' and room:
            # Kiểm tra xem có hợp đồng nào khác của phòng này đang active không
            existing_active_contract = Contract.objects.filter(
                room=room,
                status='active'
            ).exclude(pk=self.instance.pk if self.instance else None).exists()

            if existing_active_contract:
                raise serializers.ValidationError({
                    "room": _(
                        "Căn hộ này hiện đang có một hợp đồng khác đang hiệu lực (Active). Vui lòng kiểm tra lại.")
                })

        # Validate ngày tháng
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                "end_date": _("Ngày kết thúc không được nhỏ hơn ngày bắt đầu.")
            })

        return data