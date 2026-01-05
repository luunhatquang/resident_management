import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Import này để dùng cho ô tìm kiếm

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Notification
from .serializers import NotificationSerializer
from .tasks import check_expiring_contracts

# 1. API DRF (Giữ nguyên cho Swagger/Postman)
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        notif_type = self.request.query_params.get('type')
        if notif_type:
            qs = qs.filter(notification_type=notif_type)
        return qs

    @extend_schema(
        tags=["Notification"], 
        summary="Xem danh sách thông báo",
        parameters=[OpenApiParameter(name='type', type=str, description="Lọc theo loại")]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Notification"],
        summary="Tạo thông báo mới",
        responses={201: NotificationSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# 2. API Trigger thủ công (Giữ nguyên)
class ManualTriggerNotificationView(APIView):
    @extend_schema(tags=["Notification"], request=None, responses={202: None}, summary="Kích hoạt quét hợp đồng thủ công")
    def post(self, request):
        task = check_expiring_contracts.delay()
        return Response({"message": "Triggered scan", "task_id": task.id}, status=202)

# 3. API Custom cho Frontend
@login_required
@require_POST
def create_notification_api(request):
    """
    API này dùng để nhận dữ liệu từ fetch() trong file notifications.html
    """
    try:
        data = json.loads(request.body)
        
        # Lấy dữ liệu từ JSON gửi lên
        title = data.get('title')
        message = data.get('message')
        notif_type = data.get('type')
        priority = data.get('priority')

        # Tạo bản ghi mới
        new_notif = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notif_type,
            priority=priority,
            # created_by=request.user # Bỏ comment dòng này nếu model có trường người tạo
        )
        
        return JsonResponse({'status': 'success', 'id': new_notif.id})

    except Exception as e:
        print(f"Lỗi tạo thông báo: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# 4. View Render HTML (ĐÃ CẬP NHẬT BỘ LỌC)
@login_required
def getAllNotifications(request):
    # 1. Lấy tất cả dữ liệu gốc (để tính thống kê tổng quan)
    all_qs = Notification.objects.all().order_by('-created_at')
    
    # 2. Lấy tham số từ URL (Bộ lọc)
    filter_type = request.GET.get('type', 'all')
    filter_priority = request.GET.get('priority', 'all')
    search_query = request.GET.get('q', '')

    # 3. Tạo một QuerySet riêng để lọc hiển thị danh sách
    filtered_qs = all_qs

    # --- Logic Lọc ---
    if filter_type != 'all':
        filtered_qs = filtered_qs.filter(notification_type=filter_type)
    
    if filter_priority != 'all':
        filtered_qs = filtered_qs.filter(priority=filter_priority)

    if search_query:
        # Tìm kiếm trong Tiêu đề HOẶC Nội dung (không phân biệt hoa thường)
        filtered_qs = filtered_qs.filter(
            Q(title__icontains=search_query) | 
            Q(message__icontains=search_query)
        )

    # 4. Tính toán số liệu thống kê (Tính trên toàn bộ hệ thống - all_qs)
    total = all_qs.count()
    unread = all_qs.filter(is_read=False).count()
    high_priority = all_qs.filter(priority='high').count()
    emergency = all_qs.filter(priority='emergency').count()

    context = {
        'notifications': filtered_qs, # Trả về danh sách ĐÃ LỌC
        'total': total,
        'unread': unread,
        'high_priority': high_priority,
        'emergency': emergency,
        # Truyền lại giá trị lọc để HTML giữ trạng thái selected
        'current_type': filter_type,
        'current_priority': filter_priority,
        'current_query': search_query,
    }
    
    return render(request, 'notifications.html', context)

# 5. API Xử lý hành động (Đọc/Xóa)
@login_required
@require_POST
def mark_notification_as_read_api(request, pk):
    """
    API đánh dấu 1 thông báo là đã đọc
    URL: /api/notifications/<id>/read/
    """
    try:
        # Tìm thông báo theo ID (pk)
        notification = get_object_or_404(Notification, pk=pk)
        
        # Cập nhật trạng thái
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'status': 'success', 'message': 'Đã đánh dấu đã đọc'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST # Dùng POST để tương thích tốt nhất với JS fetch() hiện tại
def delete_notification_api(request, pk):
    """
    API xóa thông báo
    URL: /api/notifications/<id>/
    """
    try:
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return JsonResponse({'status': 'success', 'message': 'Đã xóa thông báo'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)