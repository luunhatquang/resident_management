from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Invoice
from resident_manage.apps.contract.models import Contract
from resident_manage.apps.building.models import Building
from .form import InvoiceForm, InvoiceUpdateForm


@login_required(login_url='login')
def getAllInvoices(request):
    invoices = Invoice.objects.select_related('room', 'resident', 'contract', 'room__building').all()
    status_filter = request.GET.get('status', '')
    service_filter = request.GET.get('service', '')
    building_filter = request.GET.get('building', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    if service_filter:
        invoices = invoices.filter(service=service_filter)
    if building_filter:
        invoices = invoices.filter(room__building_id=building_filter)
    if date_from:
        invoices = invoices.filter(start_date__gte=date_from)
    if date_to:
        invoices = invoices.filter(start_date__lte=date_to)
    if search_query:
        invoices = invoices.filter(
            Q(invoice_id__icontains=search_query) |
            Q(invoice_title__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(room__room_id__icontains=search_query) |
            Q(resident__first_name__icontains=search_query) |
            Q(resident__last_name__icontains=search_query)
        )
    
    invoices = invoices.order_by('-start_date', '-created_at')
    
    today = timezone.now()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timezone.timedelta(days=1)
    
    revenue = invoices.filter(status='paid').aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    revenue_this_month = invoices.filter(
        status='paid',
        start_date__year=today.year,
        start_date__month=today.month
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    revenue_pre_month = invoices.filter(
        status='paid',
        start_date__year=last_day_prev_month.year,
        start_date__month=last_day_prev_month.month
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    compare_revenue = (revenue_this_month - revenue_pre_month) / revenue_pre_month * 100 if revenue_pre_month != 0 else 0
    
    revenue_this_year = invoices.filter(
        status='paid',
        start_date__year=today.year
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    revenue_pre_year = invoices.filter(
        status='paid',
        start_date__year=today.year - 1,
        start_date__month=today.month
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    compare_revenue_year = (revenue_this_year - revenue_pre_year) / revenue_pre_year * 100 if revenue_pre_year != 0 else 0
    
    invoice_paid = invoices.filter(status='paid').count()
    invoice_unpaid = invoices.filter(status='unpaid').count()
    invoice_overdue = invoices.filter(status='overdue').count()
    invoice_total = invoices.count()
    
    buildings = Building.objects.all().order_by('name')
    
    context = {
        "invoices": invoices,
        "revenue": revenue,
        "revenue_this_month": revenue_this_month,
        "revenue_pre_month": revenue_pre_month,
        "compare_revenue": compare_revenue,
        "revenue_this_year": revenue_this_year,
        "revenue_pre_year": revenue_pre_year,
        "compare_revenue_year": compare_revenue_year,
        "invoice_paid": invoice_paid,
        "invoice_unpaid": invoice_unpaid,
        "invoice_overdue": invoice_overdue,
        "invoice_total": invoice_total,
        "buildings": buildings,
        "selected_status": status_filter,
        "selected_service": service_filter,
        "selected_building": building_filter,
        "search_query": search_query,
    }
    return render(request, 'invoices.html', context)


@require_http_methods(["GET"])
def get_contract_details(request, contract_id):
    """API endpoint to get contract details for auto-filling invoice form"""
    try:
        contract = Contract.objects.get(id=contract_id)
        return JsonResponse({
            'success': True,
            'room_id': contract.room.id,
            'room_name': str(contract.room),
            'resident_id': contract.resident.id,
            'resident_name': f"{contract.resident.first_name} {contract.resident.last_name}",
            'price_per_month': float(contract.price_per_month) if contract.price_per_month else 0,
        })
    except Contract.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Contract not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required(login_url='login')
def getInvoiceDetails(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    context = {"invoice": invoice}
    return render(request, 'invoice_detail.html', context)


@login_required(login_url='login')
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_all_invoices')
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form})


@login_required(login_url='login')
def update_invoice(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    if request.method == 'POST':
        form = InvoiceUpdateForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('get_invoice_details', invoice_id=invoice_id)
    else:
        form = InvoiceUpdateForm(instance=invoice)
    return render(request, 'update_invoice.html', {'form': form, 'invoice': invoice})


@login_required(login_url='login')
def deleteInvoice(request, invoice_id):
    if request.method == 'POST':
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        invoice.delete()
        return redirect('get_all_invoices')
    return redirect('get_all_invoices')


@login_required(login_url='login')
def markAsPaid(request, invoice_id):
    if request.method == 'POST':
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        invoice.status = 'paid'
        invoice.date = timezone.now().date()
        invoice.save()
        return redirect('get_all_invoices')
    return redirect('get_all_invoices')