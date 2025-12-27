from django.contrib import messages
from django.shortcuts import render, redirect
from resident_manage.apps.building.forms import  BuildingUpdateForm, RoomCreateForm, RoomUpdateForm, BuildingForm
from resident_manage.apps.building.models import Building, Room
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets


from resident_manage.apps.building.serializers import BuildingSerializer, RoomSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phép xem hoặc chỉnh sửa Buildings.
    """
    queryset = Building.objects.all().order_by('building_id')
    serializer_class = BuildingSerializer
    
class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phép xem hoặc chỉnh sửa Rooms.
    """
    queryset = Room.objects.all().order_by('room_id')
    serializer_class = RoomSerializer

@login_required(login_url='login')
def getAllBuildings(request):
    # --- PHẦN 1: THỐNG KÊ TOÀN HỆ THỐNG (Không bị ảnh hưởng bởi bộ lọc) ---
    total_buildings = Building.objects.count() # Tổng số tòa nhà trong DB
    active_count = Building.objects.filter(status='active').count()
    inactive_count = Building.objects.filter(status='inactive').count()
    
    # Tính tổng phòng (xử lý trường hợp None nếu DB rỗng)
    total_rooms_agg = Building.objects.aggregate(Sum('total_rooms'))
    total_rooms = total_rooms_agg['total_rooms__sum'] if total_rooms_agg['total_rooms__sum'] else 0

    # --- PHẦN 2: LỌC DANH SÁCH HIỂN THỊ (Bị ảnh hưởng bởi bộ lọc) ---
    buildings = Building.objects.all().order_by('-building_id') # Mặc định lấy hết

    # Lọc theo trạng thái
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        buildings = buildings.filter(status='active')
    elif status_filter == 'inactive':
        buildings = buildings.filter(status='inactive')

    # Tìm kiếm
    search_query = request.GET.get('q')
    if search_query:
        search_query = search_query.strip()
        buildings = buildings.filter(
            Q(name__icontains=search_query) | 
            Q(building_id__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    context = {
        'buildings': buildings,           # Danh sách để hiện ở lưới bên dưới
        'total_buildings': total_buildings, # <--- BIẾN MỚI: Tổng cố định
        'active_count': active_count,
        'inactive_count': inactive_count,
        'total_rooms': total_rooms,
    }
    
    return render(request, 'buildings.html', context)


@login_required(login_url='login')
def getBuildingWithFilter(request, name_contains):
    buildings = Building.objects.filter(name__icontains=name_contains)
    context = {"buildings":buildings}
    return render(request, 'buildings.html', context)

@login_required(login_url='login')
def createBuilding(request):
    """
    View xử lý thêm mới tòa nhà.
    Route: /buildings/create/
    Name: create_building
    """
    
    # 1. Xử lý khi người dùng Submit Form (POST)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        
        if form.is_valid():
<<<<<<< HEAD
            form.save()     
            return redirect('get_all_buildings')
=======
            try:
                # Lưu dữ liệu vào Database
                new_building = form.save()
                
                # Thông báo thành công
                messages.success(request, f'Đã thêm tòa nhà "{new_building.name}" thành công!')
                
                # Điều hướng về trang danh sách tòa nhà
                return redirect('get_all_buildings') 
                
            except Exception as e:
                # Xử lý lỗi hệ thống (ít gặp)
                messages.error(request, f'Có lỗi xảy ra: {e}')
        else:
            # Nếu form không hợp lệ (ví dụ thiếu trường bắt buộc), Django sẽ giữ lại dữ liệu
            # và hiển thị lỗi. Ta chỉ cần báo message chung.
            messages.error(request, 'Vui lòng kiểm tra lại thông tin nhập vào.')

    # 2. Xử lý khi người dùng truy cập trang (GET)
>>>>>>> 38612e30d27a7795c95f4f88511d5da09e8cf800
    else:
        form = BuildingForm()

    # Render template với context chứa form
    context = {
        'form': form,
        'page_title': 'Thêm Tòa nhà' # Có thể dùng để set title động
    }
    
    # Thay 'buildings/add_building.html' bằng đường dẫn thực tế file HTML thêm mới của bạn
    return render(request, "create_building.html", context)
            
@login_required(login_url='login')
def updateBuilding(request, building_id):
    building = Building.objects.get(building_id=building_id)
    if request.method == 'POST':
        form = BuildingUpdateForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('get_building_details', building_id=building_id)
    else:
        form = BuildingUpdateForm(instance=building)
    return render(request, 'update_building.html', {'form': form, 'building': building})

@login_required(login_url='login')
def getBuildingDetails(request, building_id):
    building = Building.objects.get(building_id=building_id)
    context = {"building":building}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def getBuilingsByStatus(request, status):
    buildings = Building.objects.filter(status=status)
    context = {"buildings":buildings, "status":status}
    return render(request, 'buildings.html', context)

@login_required(login_url='login')
def createRoom(request):
    # 1. Lấy thông tin tòa nhà từ URL
    initial_building_id = request.GET.get('building')
    building_obj = None
    
    if initial_building_id:
        try:
            building_obj = Building.objects.get(building_id=initial_building_id)
        except Building.DoesNotExist:
            pass

    if request.method == 'POST':
        # --- BƯỚC QUAN TRỌNG NHẤT Ở ĐÂY ---
        # Vì field building bị disabled, trình duyệt KHÔNG GỬI dữ liệu lên.
        # Ta cần tạo một bản sao của request.POST và thủ công gán building_id vào đó.
        
        post_data = request.POST.copy() # Tạo bản sao có thể chỉnh sửa
        
        if building_obj:
            # Tự động điền ID tòa nhà vào dữ liệu POST
            post_data['building'] = building_obj.pk 
            
        # Dùng post_data đã được "vá" để nạp vào form
        form = RoomCreateForm(post_data, initial={'building': building_obj})
        
        if form.is_valid():
            try:
                new_room = form.save()
                messages.success(request, f'Đã thêm phòng {new_room.room_number} thành công!')
                
                # Redirect về trang chi tiết tòa nhà (đảm bảo tên 'building_detail' đúng trong urls.py)
                return redirect('get_building_details', building_id=new_room.building.building_id)
                
            except Exception as e:
                messages.error(request, f'Lỗi hệ thống: {str(e)}')
        else:
            # In lỗi ra để debug xem tại sao form không valid
            messages.error(request, f'Vui lòng kiểm tra lại: {form.errors}')
    
    else:
        # GET Request: Chỉ cần hiển thị và disable field (logic đã có trong forms.py)
        form = RoomCreateForm(initial={'building': building_obj})

    context = {
        'form': form,
        'page_title': 'Thêm Phòng Mới'
    }
    return render(request, 'create_room.html', context)


@login_required(login_url='login')
def getRoomsByBuilding(request, building_id):
    building = Building.objects.get(building_id=building_id)
    rooms = building.rooms.all()
    context = {"building":building, "rooms":rooms}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def updateRoom(request, room_id):
    room = Room.objects.get(room_id=room_id)
    if request.method == 'POST':
        form = RoomUpdateForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('get_room_details', room_id=room_id)
    else:
        form = RoomUpdateForm(instance=room)
    return render(request, 'update_room.html', {'form': form, 'room': room})

@login_required(login_url='login')
def getAvailableRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    available_rooms = building.rooms.filter(status='available')
    context = {"building":building, "available_rooms":available_rooms}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def getUnavailableRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    unavailable_rooms = building.rooms.filter(status='unavailable')
    context = {"building":building, "unavailable_rooms":unavailable_rooms}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def getMaintenanceRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    maintenance_rooms = building.rooms.filter(status='maintenance')
    context = {"building":building, "maintenance_rooms":maintenance_rooms}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def getRoomDetails(request, room_id):
    room = Room.objects.get(room_id=room_id)
    residents = room.room_residents.all()
    context = {"room":room, "residents":residents}
    return render(request, 'room_detail.html', context)

@login_required(login_url='login')
def getRoomsByOwner(request, owner_id):
    rooms = Room.objects.filter(owner__id=owner_id)
    context = {"rooms":rooms, "owner_id":owner_id}
    return render(request, 'building_detail.html', context)

@login_required(login_url='login')
def getResidentsByRoom(request, room_id):
    room = Room.objects.get(room_id=room_id)
    residents = room.room_residents.all()
    context = {"room":room, "residents":residents}
    return render(request, 'room_detail.html', context)