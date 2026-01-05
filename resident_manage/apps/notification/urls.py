from . import views
from django.urls import path
# Nhớ import class mới tên là NotificationListCreateView nhé
from .views import NotificationListCreateView, ManualTriggerNotificationView, getAllNotifications

urlpatterns = [
    # Frontend (Giữ nguyên)
    path('notifications/', getAllNotifications, name='get_all_notifications'),
    
    # API xem VÀ tạo thông báo
    path('api/notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),

    # API kích hoạt quét hợp đồng thủ công (Giữ nguyên)
    path('api/notifications/trigger-scan/', ManualTriggerNotificationView.as_view(), name='notification-trigger'),

    path('api/notifications/create/', views.create_notification_api, name='create_notification_api'),

    # 3. API Đánh dấu đã đọc
    path('api/notifications/<str:pk>/read/', views.mark_notification_as_read_api, name='mark_notification_read'),

    # 4. API Xóa thông báo
    path('api/notifications/<str:pk>/', views.delete_notification_api, name='delete_notification'),
]