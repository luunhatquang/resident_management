from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    TYPE_ROLE = [
        ('admin', 'Admin'),
        ('staff', 'Nhân viên'),
        ('manage', 'Quản lý '),
    ]
    role = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.user.username