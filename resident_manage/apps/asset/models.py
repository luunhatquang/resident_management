from django.db import models
from resident.management.core.models.base import BaseModel
from resident.management.apps.building.models import Room, Building

class Asset(BaseModel):
    asset_id = models.CharField(max_length=50, unique=True, verbose_name="Mã tài sản")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assets', verbose_name="Phòng")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='assets', verbose_name="Tòa nhà")
    asset_name = models.CharField(max_length=100, verbose_name="Tên tài sản")
    date_maintained = models.DateField(verbose_name="Ngày bảo trì")
    TYPE_STATUS = [
        ('good', 'Tốt'),
        ('needs_repair', 'Cần sửa chữa'),
        ('broken', 'Hỏng'),
    ]
    status = models.CharField(max_length=15, choices=TYPE_STATUS, verbose_name="Trạng thái")
    detail_address = models.TextField(verbose_name="Địa chỉ chi tiết", null=True, blank=True)
    
    class Meta:
        db_table="asset"
        verbose_name = "Tài sản"
        verbose_name_plural = "Tài sản"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.asset_id} - {self.asset_name}"
    