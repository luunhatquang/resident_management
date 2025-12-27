# resident_manage/apps/resident/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.db.models import Q
from django.utils import timezone
from .models import Resident
from .form import ResidentForm


@login_required
def residents_view(request):
    """Danh sách cư dân - với tìm kiếm và lọc"""
    residents = Resident.objects.select_related('building', 'room', 'room__building').order_by('-created_at')
    
    # Đếm thống kê
    total = residents.count()
    
    # Cư dân mới trong tháng này (tức là created_at trong tháng)
    from datetime import timedelta, datetime
    from django.utils.timezone import now
    this_month = now().date().replace(day=1)
    new_residents_this_month = residents.filter(created_at__gte=this_month).count()
    
    # Cư dân chuyển đi trong tháng (hợp đồng kết thúc trong tháng)
    # from resident_manage.apps.contract.models import Contract
    # end_of_month = (this_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    # residents_moved_out_this_month = Contract.objects.filter(
    #     end_date__gte=this_month,
    #     end_date__lte=end_of_month,
    #     status__in=['expired', 'terminated']
    # ).values('resident_id').distinct().count()
    
    # Tìm kiếm
    search_keyword = request.GET.get('search', '').strip()
    if search_keyword:
        residents = residents.filter(
            Q(first_name__icontains=search_keyword) |
            Q(last_name__icontains=search_keyword) |
            Q(citizen_id__icontains=search_keyword) |
            Q(email__icontains=search_keyword) |
            Q(phone_number__icontains=search_keyword)
        )
    
    # Filter theo địa chỉ
    address_filter = request.GET.get('address', '').strip()
    if address_filter:
        residents = residents.filter(address__icontains=address_filter)
    
    # Filter theo quan hệ
    relationship_filter = request.GET.get('relationship', '').strip()
    if relationship_filter:
        residents = residents.filter(relationship=relationship_filter)
    
    # Filter theo căn hộ
    room_filter = request.GET.get('room', '').strip()
    if room_filter:
        residents = residents.filter(room__number__icontains=room_filter)
    
    # Filter theo ngày ký hợp đồng
    sign_date_from = request.GET.get('sign_date_from', '').strip()
    sign_date_to = request.GET.get('sign_date_to', '').strip()
    if sign_date_from:
        residents = residents.filter(contracts__sign_date__gte=sign_date_from)
    if sign_date_to:
        residents = residents.filter(contracts__sign_date__lte=sign_date_to)
    
    context = {
        'residents': residents.distinct() if (address_filter or relationship_filter or room_filter or sign_date_from or sign_date_to) else residents,
        'search_keyword': search_keyword,
        'address_filter': address_filter,
        'relationship_filter': relationship_filter,
        'room_filter': room_filter,
        'sign_date_from': sign_date_from,
        'sign_date_to': sign_date_to,
        'total': total,
        'new_residents_this_month': new_residents_this_month,
    }
    return render(request, 'residents.html', context)


@login_required
def resident_create_view(request):
    """Tạo cư dân mới"""
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, "Tạo cư dân thành công.")
            return redirect('residents')
    else:
        form = ResidentForm()
    
    return render(request, 'resident_form.html', {
        'form': form,
        'action': 'Tạo mới'
    })


@login_required
def resident_detail_view(request, pk):
    """Xem chi tiết cư dân"""
    resident = get_object_or_404(Resident, pk=pk)
    return render(request, 'resident_detail.html', {'resident': resident})


@login_required
def resident_edit_view(request, pk):
    """Chỉnh sửa cư dân"""
    resident = get_object_or_404(Resident, pk=pk)
    
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            message.success(request, "Cập nhật cư dân thành công.")
            return redirect('residents')
    else:
        form = ResidentForm(instance=resident)
    
    return render(request, 'resident_form.html', {
        'form': form,
        'resident': resident,
        'action': 'Chỉnh sửa'
    })


@login_required
def resident_delete_view(request, pk):
    """Xóa cư dân"""
    resident = get_object_or_404(Resident, pk=pk)
    
    if request.method == 'POST':
        resident.delete()
        message.success(request, "Xóa cư dân thành công.")
        return redirect('residents')
    
    return redirect('residents')
