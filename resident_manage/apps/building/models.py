from django.db import models
from resident_manage.core.models.base import BaseModel


class Building(BaseModel):
    building_id = models.CharField(max_length=50, unique=True, verbose_name="Mã tòa nhà")
    name = models.CharField(max_length=255, verbose_name="Tên tòa nhà")
    address = models.TextField(verbose_name="Địa chỉ")
    total_floors = models.PositiveIntegerField(verbose_name="Tổng số tầng")
    
    TYPE_STATUS = [
        ('active', 'Đang hoạt động'), 
        ('inactive', 'Ngừng hoạt động')
    ]
    status = models.CharField(max_length=10, choices=TYPE_STATUS, default='active', verbose_name="Trạng thái")
    
    class Meta:
        db_table = 'building'
        verbose_name = 'Building'
        verbose_name_plural = 'Buildings'
        ordering = ['building_id']
        
    def __str__(self):
        return f"{self.name} - {self.building_id}"
    
class Room(BaseModel):
    room_id = models.CharField(max_length=50, unique=True, verbose_name="Mã căn hộ")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms', verbose_name='Tòa nhà')
    floor_number = models.PositiveIntegerField(verbose_name="Số tầng")
    room_number = models.CharField(max_length=10, verbose_name="Số phòng")
    
    TYPE_STATUS = [
        ('available', 'Đang trống'),
        ('unavailable', 'Không còn trống')
    ]
    status = models.CharField(max_length=12, choices=TYPE_STATUS, default='available', verbose_name="Trạng thái")
    
    LISTING_TYPE = [
        ('rent', 'Cho thuê'), 
        ('sale', 'Bán')
    ]
    type_listing = models.CharField(max_length=10, choices=LISTING_TYPE, verbose_name="Loại hình")
    
    class Meta:
        db_table = 'room'
        verbose_name = 'Căn hộ'
        verbose_name_plural = 'Căn hộ'
        ordering = ['building', 'floor_number', 'room_number']
    
    def __str__(self):
        return f"{self.building.name} - Tầng {self.floor_number} - Phòng {self.room_number}"