from django.db import models
from resident_manage.core.models.base import BaseModel
from resident_manage.apps.building.models import Room, Building
from resident_manage.apps.contract.models import Contract
from resident_manage.apps.resident.models import Resident


class OperationExpense(BaseModel):
    expense_id = models.CharField(max_length=50, unique=True, verbose_name="Mã chi phí")
    expense_title = models.CharField(max_length=255, verbose_name="Nội dung chi phí")
    TYPE_CATEGORY = [
        ('maintenance', 'Chi phí bảo trì'),
        ('utilities', 'Chi phí tiện ích'),
        ('salaries', 'Chi phí lương nhân viên'),
        ('security', 'Chi phí an ninh'),
        ('cleaning','Chi phí vệ sinh'),
        ('supplies', 'Chi phí vật tư'),
        ('other', 'Chi phí khác'),
    ]
    category_type = models.CharField(max_length=20, choices=TYPE_CATEGORY, verbose_name="Loại chi phí")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='operation_expenses', verbose_name="Tòa nhà")
    date = models.DateField(verbose_name="Ngày chi phí")
    count = models.IntegerField(verbose_name="Số lượng", default=1)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Số tiền/đơn vị (VNĐ)")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tổng tiền (VNĐ)", editable=False)
    TYPE_STATUS = [
        ('paid', 'Đã thanh toán'),
        ('unpaid', 'Chưa thanh toán'),
        ('overdue', 'Quá hạn'),
    ]
    status = models.CharField(max_length=10, choices=TYPE_STATUS, verbose_name="Trạng thái", default='unpaid')
    description = models.TextField(verbose_name="Ghi chú", blank=True, default='')
    recorded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='recorded_expenses', verbose_name="Người ghi nhận", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.count * self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.expense_id} - {self.expense_title}"

    class Meta:
        verbose_name = "Chi phí vận hành"
        verbose_name_plural = "Chi phí vận hành"
