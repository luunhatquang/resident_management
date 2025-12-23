from django.db import models
from resident_management.core.models.base import BaseModel
from resident_management.apps.resident.models import Resident
from resident_management.apps.building.models import Room

class Contract(BaseModel):
    contract_id = models.CharField(max_length=50, unique=True, verbose_name="Mã hợp đồng")
    
    TYPE_CONTRACT = [
        ('rent', 'Hợp đồng thuê'), 
        ('sale', 'Hợp đồng mua bán')
    ]
    contract_type = models.CharField(max_length=10, choices=TYPE_CONTRACT, verbose_name="Loại hợp đồng")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc", null=True, blank=True)
    sign_date = models.DateField(verbose_name="Ngày ký")
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='contracts', verbose_name="Cư dân")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='contracts', verbose_name="Căn hộ")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tổng giá trị (VNĐ)")
    price_per_month = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Giá thuê/tháng (VNĐ)", null=True, blank=True)
    deposit = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tiền cọc (VNĐ)", null=True, blank=True)
    
    STATUS_CONTRACT = [
        ('pending', 'Đang chờ duyệt'),
        ('active', 'Đang hiệu lực'),
        ('expired', 'Đã hết hạn'),
        ('terminated', 'Đã chấm dứt'),
        ('rejected', 'Từ chối'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CONTRACT, verbose_name="Trạng thái", default='pending')
    
    class Meta:
        db_table = "contract"
        verbose_name = "Hợp đồng"
        verbose_name_plural = "Hợp đồng"
        ordering = ['-sign_date']
    
    def __str__(self):
        return f"{self.contract_id} - {self.resident.first_name} {self.resident.last_name}"
