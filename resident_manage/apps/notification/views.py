from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import check_expiring_contracts


# Frontend View
@login_required(login_url='login')
def getAllNotifications(request):
    notifications = Notification.objects.all()
    
    # Stats
    total = notifications.count()
    unread = notifications.filter(is_read=False).count()
    high_priority = notifications.filter(priority='high').count()
    emergency = notifications.filter(priority='emergency').count()
    
    context = {
        'notifications': notifications,
        'total': total,
        'unread': unread,
        'high_priority': high_priority,
        'emergency': emergency,
    }
    return render(request, 'notifications.html', context)


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        notif_type = self.request.query_params.get('type')
        if notif_type:
            qs = qs.filter(notification_type=notif_type)
        return qs

    @extend_schema(tags=["Notification"], parameters=[OpenApiParameter(name='type', type=str)])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ManualTriggerNotificationView(APIView):
    @extend_schema(tags=["Notification"], request=None, responses={202: None})
    def post(self, request):
        task = check_expiring_contracts.delay()
        return Response({"message": "Triggered scan", "task_id": task.id}, status=202)
