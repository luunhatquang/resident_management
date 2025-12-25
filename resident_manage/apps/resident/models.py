from django.db import models
from resident_manage.core.models.base import BaseModel
from resident_manage.apps.building.models import Building, Room

class Resident(BaseModel):
    citizen_id = models.CharField(max_length=20, unique=True, verbose_name="Số CMND/CCCD")
    first_name = models.CharField(max_length=50, verbose_name="Tên")
    last_name = models.CharField(max_length=50, verbose_name="Họ")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Giới tính")
    phone_number = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(max_length=100, verbose_name="Email", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    
    RELATIONSHIP_CHOICES = [
        ('owner', 'Chủ hộ'),
        ('spouse', 'Vợ/Chồng'),
        ('child', 'Con'),
        ('parent', 'Bố/Mẹ'),
        ('relative', 'Người thân'),
        ('tenant', 'Khách thuê'),
        ('other', 'Khác'),
    ]
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='tenant', verbose_name="Quan hệ với chủ hộ")
    
    building = models.ForeignKey('building.Building', on_delete=models.PROTECT, related_name='residents', verbose_name="Tòa nhà", null=True, blank=True)
    room = models.ForeignKey('building.Room', on_delete=models.PROTECT, related_name='residents', verbose_name="Căn hộ", null=True, blank=True)
    class Meta:
        db_table = "resident"
        verbose_name = "Cư dân"
        verbose_name_plural = "Cư dân"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.citizen_id})"