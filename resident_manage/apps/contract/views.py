from django.shortcuts import render, redirect, get_object_or_404 
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django.contrib import messages as message
from django.contrib.auth.decorators import login_required
from .models import Contract
from .form import ContractForm 


@login_required
def contracts_view(request):
    contracts = Contract.objects.select_related('resident', 'room', 'room__building')
    today = timezone.now().date()
    
    filter_type = request.GET.get('type')
    if filter_type in ['rent', 'sale']:
        contracts = contracts.filter(contract_type=filter_type)
    
    filter_status = request.GET.get('status')
    if filter_status:
        contracts = contracts.filter(status=filter_status)
    
    search_keyword = request.GET.get('search', '').strip()
    if search_keyword:
        contracts = contracts.filter(
            Q(contract_id__icontains=search_keyword) |
            Q(resident__first_name__icontains=search_keyword) |
            Q(resident__last_name__icontains=search_keyword) |
            Q(resident__citizen_id__icontains=search_keyword) |
            Q(room__room_id__icontains=search_keyword) |
            Q(room__room_number__icontains=search_keyword) |
            Q(room__building__name__icontains=search_keyword)
        )
    
    is_expired = contracts.filter(status='expired').count()
    will_expire = contracts.filter(
        status='will_expire'
    ).count()
    is_active = contracts.filter(
        status='active',
    ).count()
    pending = contracts.filter(status='pending').count()
    
    context = {
        'total': contracts.count(),
        'contracts': contracts.order_by('-created_at'),
        'is_expired': is_expired,
        'is_active': is_active,
        'will_expire': will_expire,
        'pending': pending,
        'filter_type': filter_type or '',
        'filter_status': filter_status or '',
        'search_keyword': search_keyword,
    }
    
    return render(request, 'contracts.html', context)

@login_required
def contract_create_view(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, "Tạo hợp đồng thành công.")
            return redirect('contracts')
    else:
        form = ContractForm()
    return render(request, 'contract_form.html', {'form': form, 'action': 'Tạo mới'})

@login_required  
def contract_edit_view(request,pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            message.success(request, "Cập nhật hợp đồng thành công.")
            return redirect('contracts')
    else:
        form = ContractForm(instance=contract)
    return render(request, 'contract_form.html', {'form': form, 'contract': contract,'action': 'Chỉnh sửa'})

@login_required
def contract_detail_view(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    return render(request, 'contract_detail.html', {'contract': contract})

@login_required
def contract_delete_view(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == 'POST':
        contract.delete()
        message.success(request, "Xóa hợp đồng thành công.")
        return redirect('contracts')
    return redirect('contracts')