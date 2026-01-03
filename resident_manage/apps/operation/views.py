from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils import timezone
from .models import OperationExpense
from resident_manage.apps.building.models import Building
from .forms import OperationExpenseForm


@login_required 
def get_all_expenses(request):
    expenses = OperationExpense.objects.all()
    building_filter = request.GET.get('building', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    recorded_by_filter = request.GET.get('recorded_by', '')
    category_filter = request.GET.get('category_type', '')
    
    if building_filter:
        expenses = expenses.filter(building__id=building_filter)
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)
    if recorded_by_filter:
        expenses = expenses.filter(recorded_by__id=recorded_by_filter)
    if category_filter:
        expenses = expenses.filter(category_type=category_filter)
        
    expenses = expenses.order_by('-date', '-created_at')
    
    total_expenses = expenses.aggregate(total=Sum('total_amount'))['total'] or 0
    total_paid = expenses.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    count_paid = expenses.filter(status='paid').count()
    
    total_maintaince = expenses.filter(category_type='maintenance').aggregate(total=Sum('total_amount'))['total'] or 0
    total_utilities = expenses.filter(category_type='utilities').aggregate(total=Sum('total_amount'))['total'] or 0
    total_salaries = expenses.filter(category_type='salaries').aggregate(total=Sum('total_amount'))['total'] or 0
    total_security = expenses.filter(category_type='security').aggregate(total=Sum('total_amount'))['total'] or 0
    total_cleaning = expenses.filter(category_type='cleaning').aggregate(total=Sum('total_amount'))['total'] or 0
    total_supplies = expenses.filter(category_type='supplies').aggregate(total=Sum('total_amount'))['total'] or 0
    total_other = expenses.filter(category_type='other').aggregate(total=Sum('total_amount'))['total'] or 0
    
    today = timezone.now()
    total_paid_this_month = expenses.filter(
        status='paid',
        date__month=today.month,
        date__year=today.year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timezone.timedelta(days=1)
    
    total_paid_pre_month = expenses.filter(
        status='paid',
        date__month=last_day_prev_month.month,
        date__year=last_day_prev_month.year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Lấy danh sách users đã từng thêm chi phí
    users_with_expenses = User.objects.filter(
        recorded_expenses__isnull=False
    ).distinct().order_by('username')
    
    # Lấy danh sách buildings
    buildings = Building.objects.all().order_by('name')
         
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'total_paid': total_paid,
        'count_paid': count_paid,
        'total_maintaince': total_maintaince,
        'total_utilities': total_utilities,
        'total_salaries': total_salaries,
        'total_security': total_security,
        'total_cleaning': total_cleaning,
        'total_supplies': total_supplies,
        'total_other': total_other,
        'total_paid_this_month': total_paid_this_month,
        'total_paid_pre_month': total_paid_pre_month,
        'users': users_with_expenses,
        'buildings': buildings,
        'selected_user': recorded_by_filter,
        'selected_building': building_filter,
        'selected_category': category_filter,
        'category_choices': OperationExpense.TYPE_CATEGORY,
    }
    return render(request, 'operation/expenses.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = OperationExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.recorded_by = request.user
            expense.save()
            return redirect('get_all_expenses')
    else:
        form = OperationExpenseForm(initial={'date': timezone.now().date()})
    return render(request, 'operation/add_expense.html', {'form': form, 'action': 'Thêm mới'})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(OperationExpense, pk=pk)
    if request.method == 'POST':
        form = OperationExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('get_all_expenses')
    else:
        form = OperationExpenseForm(instance=expense)
    return render(request, 'operation/edit_expense.html', {'form': form, 'expense': expense, 'action': 'Chỉnh sửa'})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(OperationExpense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('get_all_expenses')
    return render(request, 'operation/delete_expense.html', {'expense': expense})

@login_required
def view_expense(request, pk):
    expense = get_object_or_404(OperationExpense, pk=pk)
    return render(request, 'operation/view_expense.html', {'expense': expense})
