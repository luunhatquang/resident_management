from django.db import models
from resident_management.core.models.base import BaseModel
from resident_management.apps.resident.models import Resident
from resident_management.apps.building.models import Room, Building
from resident_management.apps.contract.models import Contract




class Notification(BaseModel):
    
    TYPE_CHOICE = [
        ('contract_expiring','Hợp đồng sắp hết hạn'),
        ('contract_expired','Hợp đồng đã hết hạn'),
        ('payment_reminder','Nhắc nhở thanh toán dịch vụ'),
        ('maintenance','Thông báo bảo trì'),
        ('general','Thông báo chung'),
    ]
    
    PRIORITY_CHOICE = [
        ('low','Thấp'),
        ('medium','Trung bình'),
        ('high','Cao'),
        ('emergency', 'Khẩn cấp'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    message = models.TextField(verbose_name="Nội dung")
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICE, verbose_name="Loại thông báo")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICE, verbose_name="Độ ưu tiên")
    
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name='notifications', verbose_name="Hợp đồng liên quan", null=True, blank=True)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='notifications', verbose_name="Cư dân nhận thông báo", null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='notifications', verbose_name="Tòa nhà nhận thông báo", null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='notifications', verbose_name="Căn hộ nhận thông báo", null=True, blank=True)
    
    send_at = models.DateTimeField(verbose_name="Thời gian gửi", null=True, blank=True)
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")
    
    class Meta:
        db_table = "notification"
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type', 'priority']),   
        ]
        
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    
    