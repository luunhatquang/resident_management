"""
Context processors for templates
"""
from django.contrib.auth.models import AnonymousUser
from resident_manage.apps.notification.models import Notification


def notification_context(request):
    """
    Add unread notification count to all templates
    """
    if isinstance(request.user, AnonymousUser):
        return {'unread_count': 0}
    
    unread_count = Notification.objects.filter(is_read=False).count()
    return {'unread_count': unread_count}

