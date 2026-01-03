from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging
from resident_manage.apps.contract.models import Contract
from resident_manage.apps.notification.models import Notification

logger = logging.getLogger(__name__)

@shared_task
def check_expiring_contracts():
    today = timezone.now().date()
    target_date = today + timedelta(days=7)

    expiring_contracts = Contract.objects.filter(
        status='active',
        end_date__range=[today, target_date]
    ).select_related('resident', 'room', 'room__building')

    count = 0
    for contract in expiring_contracts:
        exists = Notification.objects.filter(
            contract=contract,
            notification_type='contract_expiring',
            created_at__date=today
        ).exists()

        if not exists:
            Notification.objects.create(
                title="⚠️ Nhắc nhở: Hợp đồng sắp hết hạn",
                message=f"Hợp đồng {contract.contract_id} của căn hộ {contract.room} sắp hết hạn vào {contract.end_date}.",
                notification_type='contract_expiring',
                priority='high',
                contract=contract,
                resident=contract.resident,
                room=contract.room,
                building=contract.room.building if contract.room else None,
                send_at=timezone.now()
            )
            count += 1
    
    return f"Đã tạo {count} thông báo nhắc hạn."