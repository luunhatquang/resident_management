from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from resident_manage.apps.resident.models import Resident
from resident_manage.apps.building.models import Room, Building
from resident_manage.apps.invoice.models import Invoice


def room_detail_api(request, room_id):
    try:
        room = Room.objects.select_related('building').get(id=room_id)
        residents = Resident.objects.filter(room=room)
        
        resident_list = []
        for r in residents:
            resident_list.append({
                'name': f"{r.last_name} {r.first_name}",
                'citizen_id': r.citizen_id,
                'phone_number': r.phone_number,
                'email': r.email,
                'address': r.address,
                'role': r.get_relationship_display(),
            })
            
        data = {
            'room_number': room.room_number,
            'floor_number': room.floor_number,
            'area': str(room.room_area),
            'status': room.get_status_display(),
            'status_code': room.status,
            'residents': resident_list,
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy phòng'}, status=404)


@login_required
def dashboard_view(request):
    building_name = request.GET.get('building')
    active_building = None
    if building_name:
        active_building = Building.objects.filter(name=building_name).first()
    
    if active_building:
        rooms = Room.objects.filter(building=active_building)
    else:
        active_building = Building.objects.first()
        if active_building:
            rooms = Room.objects.filter(building=active_building)
        else:
            rooms = Room.objects.none()
            
    all_rooms = Room.objects.all()
    room_empty_count = all_rooms.filter(status='available').count()
    room_occupied_count = all_rooms.filter(status='unavailable').count()
    
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.now()
    revenue_data = Invoice.objects.filter(
        status='paid', 
        date__year=today.year, 
        date__month=today.month
    ).aggregate(total=Sum('total_price'))
    revenue = revenue_data['total'] or 0
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    prev_revenue_data = Invoice.objects.filter(
        status='paid',
        date__year=last_day_prev_month.year,
        date__month=last_day_prev_month.month
    ).aggregate(total=Sum('total_price'))
    prev_revenue = prev_revenue_data['total'] or 0
    
    revenue_growth = 0
    if prev_revenue > 0:
        revenue_growth = ((revenue - prev_revenue) / prev_revenue) * 100
    
    floors = []
    if active_building:
        for f in range(1, active_building.total_floors + 1):
            floor_rooms = rooms.filter(floor_number=f).order_by('room_number')
            if floor_rooms.exists():
                floors.append({
                    'number': f,
                    'rooms': floor_rooms
                })
    
    context = {
        'revenue': revenue,
        'revenue_growth': round(revenue_growth, 1),
        'room_total': all_rooms.filter(building=active_building).count(),
        'room_empty_count': room_empty_count,
        'room_occupied_count': room_occupied_count,
        'buildings': Building.objects.all(),
        'active_building': active_building,
        'floors': floors,
        'building_name': building_name or 'Toàn bộ toà nhà'
    }

    return render(request, 'dashboard.html', context)


@login_required
def contracts_view(request):
    return render(request, 'contracts.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')
