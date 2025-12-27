from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Invoice
from resident_manage.apps.contract.models import Contract
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .form import InvoiceForm, InvoiceUpdateForm


@login_required(login_url='login')
def getAllInvoices(request):
    invoice = Invoice.objects.all()
    today = timezone.now()
    
    # Tổng doanh thu (tất cả đã thanh toán)
    revenue = 0
    for i in invoice:
        if i.status == 'paid':
            revenue += i.total_price
    
    # Doanh thu tháng này (dựa vào start_date - kỳ thu phí)
    revenue_this_month = 0
    for i in invoice:
        if i.status == 'paid' and i.start_date.month == today.month and i.start_date.year == today.year:
            revenue_this_month += i.total_price
    
    # Doanh thu tháng trước
    revenue_pre_month = 0
    prev_month = today.month - 1 if today.month > 1 else 12
    prev_month_year = today.year if today.month > 1 else today.year - 1
    for i in invoice:
        if i.status == 'paid' and i.start_date.month == prev_month and i.start_date.year == prev_month_year:
            revenue_pre_month += i.total_price
    
    # So sánh với tháng trước
    compare_revenue = (revenue_this_month - revenue_pre_month)/revenue_pre_month * 100 if revenue_pre_month != 0 else 0
    
    # Doanh thu năm nay
    revenue_this_year = 0
    for i in invoice:
        if i.status == 'paid' and i.start_date.year == today.year:
            revenue_this_year += i.total_price
    
    # Doanh thu năm trước (cùng tháng)
    revenue_pre_year = 0
    for i in invoice:
        if i.status == 'paid' and i.start_date.year == (today.year - 1) and i.start_date.month == today.month:
            revenue_pre_year += i.total_price
    
    # So sánh với năm trước
    compare_revenue_year = (revenue_this_year - revenue_pre_year)/revenue_pre_year * 100 if revenue_pre_year != 0 else 0
    
    # Thống kê số lượng hóa đơn
    invoice_paid = invoice.filter(status='paid').count()
    invoice_unpaid = invoice.filter(status='unpaid').count()
    invoice_overdue = invoice.filter(status='overdue').count()
    invoice_total = invoice.count()
    context = {
        "invoices": invoice,
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