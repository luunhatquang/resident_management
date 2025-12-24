from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Contract
from .serializers import ContractSerializer
from resident_management.core.utils.response import success, error


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'contract_type', 'resident', 'room']
    search_fields = ['contract_id', 'resident__first_name', 'resident__last_name', 'room__room_number']
    ordering_fields = ['sign_date', 'created_at']
    ordering = ['-created_at']

    @extend_schema(
        summary="Tạo hợp đồng mới",
        description="Tạo hợp đồng thuê hoặc mua bán. Hệ thống sẽ kiểm tra xem căn hộ đã có hợp đồng active chưa.",
        examples=[
            OpenApiExample(
                'Ví dụ tạo hợp đồng',
                value={
                    "contract_id": "HD-2023-001",
                    "contract_type": "rent",
                    "start_date": "2023-12-01",
                    "end_date": "2024-12-01",
                    "sign_date": "2023-11-25",
                    "resident": 1,
                    "room": 10,
                    "total_price": "120000000",
                    "price_per_month": "10000000",
                    "deposit": "20000000",
                    "status": "active"
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Đóng hợp đồng (Thanh lý)",
        description="Chuyển trạng thái hợp đồng sang 'terminated' (Đã chấm dứt).",
        request=None,
        responses={200: ContractSerializer}
    )
    @action(detail=True, methods=['put'], url_path='close')
    def close_contract(self, request, pk=None):
        contract = self.get_object()

        if contract.status in ['terminated', 'expired', 'rejected']:
            return Response(
                error(message="Hợp đồng này đã kết thúc hoặc không hợp lệ để đóng."),
                status=status.HTTP_400_BAD_REQUEST
            )

        contract.status = 'terminated'
        contract.save()

        # Có thể thêm logic cập nhật trạng thái phòng về 'available' tại đây nếu cần
        # contract.room.status = 'available'
        # contract.room.save()

        serializer = self.get_serializer(contract)
        return Response(
            success(data=serializer.data, message="Đã đóng hợp đồng thành công.")
        )