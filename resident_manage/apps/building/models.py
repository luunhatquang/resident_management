from django.db import models
from resident_manage.core.models.base import BaseModel
# from resident_manage.apps.resident.models import Resident


class Building(BaseModel):
    building_id = models.CharField(max_length=50, unique=True, verbose_name="Mã tòa nhà")
    name = models.CharField(max_length=255, verbose_name="Tên tòa nhà")
    address = models.TextField(verbose_name="Địa chỉ")
    total_floors = models.PositiveIntegerField(verbose_name="Tổng số tầng", null=True, blank=True)
    total_rooms = models.PositiveIntegerField(verbose_name="Tổng số phòng", null=True, blank=True)
    total_availble_rooms = models.PositiveIntegerField(verbose_name="Số phòng còn trống", null=True, blank=True)   


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
    owner = models.ForeignKey('resident.Resident', on_delete=models.SET_NULL, null=True, blank=True, related_name='room_owner', verbose_name="Chủ sở hữu")    
    floor_number = models.PositiveIntegerField(verbose_name="Số tầng")
    room_number = models.CharField(max_length=10, verbose_name="Số phòng")
    room_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diện tích phòng")
    bedroom_count = models.PositiveIntegerField(verbose_name="Số phòng ngủ")
    bathroom_count = models.PositiveIntegerField(verbose_name="Số phòng tắm")
    room_residents = models.ManyToManyField('resident.Resident', related_name='room_residents', blank=True, verbose_name="Thành viên")
    rent_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Giá thuê", default=0.0)

    TYPE_STATUS = [
        ('available', 'Đang trống'),
        ('unavailable', 'Không còn trống'),
        ('maintenance', 'Bảo trì')
    ]
    status = models.CharField(max_length=12, choices=TYPE_STATUS, default='available', verbose_name="Trạng thái")
    
    LISTING_TYPE = [
        ('rent', 'Cho thuê'), 
        ('sale', 'Bán')
    ]
    type_listing = models.CharField(max_length=10, choices=LISTING_TYPE, verbose_name="Loại hình kinh doanh")
    
    class Meta:
        db_table = 'room'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['building', 'floor_number', 'room_number']
    
    def __str__(self):
        return f"Phòng {self.room_number} - Tầng {self.floor_number} - Tòa nhà {self.building.name}"
        
    @property
    def active_contract(self):
        return self.contracts.filter(status__in=['active', 'will_expire']).first()