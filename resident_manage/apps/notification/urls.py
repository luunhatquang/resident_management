from django.urls import path
from .views import NotificationListView, ManualTriggerNotificationView

# Vì chúng ta dùng APIView lẻ (Custom View) nên không cần DefaultRouter
urlpatterns = [
    # 1. API xem danh sách thông báo
    # Đường dẫn thực tế: /api/notifications/
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # 2. API kích hoạt quét hợp đồng thủ công (Admin bấm nút)
    # Đường dẫn thực tế: /api/notifications/trigger-scan/
    path('notifications/trigger-scan/', ManualTriggerNotificationView.as_view(), name='notification-trigger'),
]