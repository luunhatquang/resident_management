from django.db import models
from resident_manage.core.models.base import BaseModel
from resident_manage.apps.building.models import Room
from resident_manage.apps.contract.models import Contract


class Invoice(BaseModel):
    invoice_id = models.CharField(max_length=50, unique=True, verbose_name="Mã hóa đơn")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invoices', verbose_name="Phòng")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='invoices', verbose_name="Hợp đồng", null=True, blank=True)
    TYPE_SERVICE = [
        ('electricity', 'Hoá đơn điện'),
        ('water', 'Hoá đơn nước'),
        ('internet', 'Hoá đơn internet'),
        ('rent', 'Hoá đơn tiền thuê phòng'),
        ('maintenance', 'Hoá đơn bảo trì'),
        ('other', 'Hoá đơn khác'),
    ]
    service = models.CharField(max_length=20, choices=TYPE_SERVICE, verbose_name="Dịch vụ")
    count_unit = models.IntegerField(verbose_name="Số lượng đơn vị", default=1)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Đơn giá (VNĐ)")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tổng tiền (VNĐ)")
    TYPE_STATUS = [
        ('paid', 'Đã thanh toán'),
        ('unpaid', 'Chưa thanh toán'),
        ('overdue', 'Quá hạn'),
    ]
    status = models.CharField(max_length=10, choices=TYPE_STATUS, verbose_name="Trạng thái")
    start_date = models.DateField(verbose_name="Ngày thu phí")
    date = models.DateField(verbose_name="Ngày nộp phí", null=True, blank=True)
    end_date = models.DateField(verbose_name="Ngày hết hạn", null=True, blank=True)

    class Meta:
        db_table = "invoice"
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service', 'status']),
        ]

    def __str__(self):
        return f"{self.invoice_id} - {self.get_service_display()} - {self.get_status_display()}"



    