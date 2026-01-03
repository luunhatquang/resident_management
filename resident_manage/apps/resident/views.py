# resident_manage/apps/resident/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now
import json
from .models import Resident
from .form import ResidentForm


@login_required
def residents_view(request):
    """Danh sách cư dân - với tìm kiếm và lọc"""
    residents = Resident.objects.select_related('building', 'room', 'room__building').order_by('-created_at')
    
    # Đếm thống kê
    total = residents.count()
    living_total = residents.filter(status='living').count()
    
    # Cư dân mới trong tháng này (tức là created_at trong tháng)
    this_month = now().date().replace(day=1)
    new_residents_this_month = residents.filter(created_at__gte=this_month).count()
    living_new_residents_this_month = residents.filter(status='living', created_at__gte=this_month).count()
    
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
        # Tìm kiếm theo display name của status và relationship
        status_q = Q()
        for key, display in Resident.STATUS_CHOICES:
            if search_keyword.lower() in display.lower():
                status_q |= Q(status=key)
        
        relationship_q = Q()
        for key, display in Resident.RELATIONSHIP_CHOICES:
            if search_keyword.lower() in display.lower():
                relationship_q |= Q(relationship=key)
        
        residents = residents.filter(
            Q(first_name__icontains=search_keyword) |
            Q(last_name__icontains=search_keyword) |
            Q(citizen_id__icontains=search_keyword) |
            Q(email__icontains=search_keyword) |
            Q(phone_number__icontains=search_keyword) |
            Q(address__icontains=search_keyword) |
            status_q |
            relationship_q |
            Q(building__name__icontains=search_keyword) |
            Q(room__room_number__icontains=search_keyword)
        )
    
    # Filter theo trạng thái
    status_filter = request.GET.get('status', '').strip()
    if status_filter and status_filter in dict(Resident.STATUS_CHOICES):
        residents = residents.filter(status=status_filter)
    
    context = {
        'residents': residents,
        'search_keyword': search_keyword,
        'status_filter': status_filter,
        'status_choices': Resident.STATUS_CHOICES,
        'total': total,
        'living_total': living_total,
        'new_residents_this_month': new_residents_this_month,
        'living_new_residents_this_month': living_new_residents_this_month,
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


@login_required
@require_http_methods(["POST", "PATCH"])
def resident_update_status_view(request, pk):
    """Cập nhật trạng thái cư dân"""
    resident = get_object_or_404(Resident, pk=pk)
    
    try:
        data = json.loads(request.body)
        status = data.get('status')
        
        if status and status in dict(Resident.STATUS_CHOICES):
            resident.status = status
            resident.save()
            return JsonResponse({'success': True, 'message': 'Cập nhật trạng thái thành công'})
        else:
            return JsonResponse({'success': False, 'message': 'Trạng thái không hợp lệ'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dữ liệu không hợp lệ'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
