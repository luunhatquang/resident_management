from django.urls import path
from .views import NotificationListView, ManualTriggerNotificationView, getAllNotifications

# Vì chúng ta dùng APIView lẻ (Custom View) nên không cần DefaultRouter
urlpatterns = [
    # Frontend
    path('notifications/', getAllNotifications, name='get_all_notifications'),
    
    # API xem danh sách thông báo
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),

    # API kích hoạt quét hợp đồng thủ công (Admin bấm nút)
    path('api/notifications/trigger-scan/', ManualTriggerNotificationView.as_view(), name='notification-trigger'),
]