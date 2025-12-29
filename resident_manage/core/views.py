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
            'room_id': room.room_id,
            'room_number': room.room_number,
            'floor_number': room.floor_number,
            'building_name': room.building.name,
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
    show_all_buildings = False
    active_building = None
    if building_name and building_name != 'Toàn bộ tòa nhà':
        active_building = Building.objects.filter(name=building_name).first()
        rooms = Room.objects.filter(building=active_building) if active_building else Room.objects.none()
    else:
        show_all_buildings = True
        rooms = Room.objects.select_related('building').all()
    if show_all_buildings:
        all_rooms = Room.objects.all()
        room_total = all_rooms.count()
        room_empty_count = all_rooms.filter(status='available').count()
        room_occupied_count = all_rooms.filter(status='unavailable').count()
    else:
        if active_building:
            all_rooms = Room.objects.filter(building=active_building)
            room_total = all_rooms.count()
            room_empty_count = all_rooms.filter(status='available').count()
            room_occupied_count = all_rooms.filter(status='unavailable').count()
        else:
            room_total = 0
            room_empty_count = 0
            room_occupied_count = 0
    
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
    
    buildings_data = []
    if show_all_buildings:
        buildings_list = Building.objects.all().order_by('building_id')
        for building in buildings_list:
            building_rooms = rooms.filter(building=building)
            if building_rooms.exists():
                floors = []
                max_floors = building.total_floors or 0
                for f in range(1, max_floors + 1):
                    floor_rooms = building_rooms.filter(floor_number=f).order_by('room_number')
                    if floor_rooms.exists():
                        floors.append({
                            'number': f,
                            'rooms': floor_rooms
                        })
                if floors:
                    buildings_data.append({
                        'building': building,
                        'floors': floors
                    })
    else:
        if active_building:
            floors = []
            max_floors = active_building.total_floors or 0
            for f in range(1, max_floors + 1):
                floor_rooms = rooms.filter(floor_number=f).order_by('room_number')
                if floor_rooms.exists():
                    floors.append({
                        'number': f,
                        'rooms': floor_rooms
                    })
            if floors:
                buildings_data.append({
                    'building': active_building,
                    'floors': floors
                })
    
    context = {
        'revenue': revenue,
        'revenue_growth': round(revenue_growth, 1),
        'room_total': room_total,
        'room_empty_count': room_empty_count,
        'room_occupied_count': room_occupied_count,
        'buildings': Building.objects.all(),
        'active_building': active_building,
        'buildings_data': buildings_data,
        'show_all_buildings': show_all_buildings,
        'building_name': building_name or 'Toàn bộ tòa nhà'
    }

    return render(request, 'dashboard.html', context)


@login_required
def contracts_view(request):
    return render(request, 'contracts.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')
