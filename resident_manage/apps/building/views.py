from django.shortcuts import render
from resident_manage.apps.building.forms import BuildingCreateForm, BuildingUpdateForm, RoomCreateForm, RoomUpdateForm
from resident_manage.apps.building.models import Building, Room
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
    buildings = Building.objects.all()
    context = {"buildings":buildings}
    return render(request, '', context)

@login_required(login_url='login')
def getBuildingWithFilter(request, name_contains):
    buildings = Building.objects.filter(name__icontains=name_contains)
    context = {"buildings":buildings}
    return render(request, '', context)

@login_required(login_url='login')
def createBuilding(request):
    if request.method == 'POST':
        form = BuildingCreateForm(request.POST)
        if form.is_valid():
            form.save()     
            
@login_required(login_url='login')
def updateBuilding(request, building_id):
    if request.method == 'POST':
        form = BuildingUpdateForm(request.POST)
        if form.is_valid():
            # building = Building.objects.get(building_id=building_id)
            # building.name = form.cleaned_data['name']
            # building.address = form.cleaned_data['address']
            # building.num_floors = form.cleaned_data['num_floors']
            # building.status = form.cleaned_data['status']
            form.save()

@login_required(login_url='login')
def getBuildingDetails(request, building_id):
    building = Building.objects.get(building_id=building_id)
    context = {"building":building}
    return render(request, '', context)

@login_required(login_url='login')
def getBuilingsByStatus(request, status):
    buildings = Building.objects.filter(status=status)
    context = {"buildings":buildings, "status":status}
    return render(request, '', context)

@login_required(login_url='login')
def createRoom(request):
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            form.save()


@login_required(login_url='login')
def getRoomsByBuilding(request, building_id):
    building = Building.objects.get(building_id=building_id)
    rooms = building.rooms.all()
    context = {"building":building, "rooms":rooms}
    return render(request, '', context)

@login_required(login_url='login')
def updateRoom(request, room_id):
    if request.method == 'POST':
        form = RoomUpdateForm(request.POST)
        if form.is_valid():
            room = Room.objects.get(room_id=room_id)
            room.status = form.cleaned_data['status']
            room.owner = form.cleaned_data['owner']
            room.room_residents.set(form.cleaned_data['residents'])
            room.save()

@login_required(login_url='login')
def getAvailableRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    available_rooms = building.rooms.filter(status='available')
    context = {"building":building, "available_rooms":available_rooms}
    return render(request, '', context)

@login_required(login_url='login')
def getUnavailableRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    unavailable_rooms = building.rooms.filter(status='unavailable')
    context = {"building":building, "unavailable_rooms":unavailable_rooms}
    return render(request, '', context)

@login_required(login_url='login')
def getMaintenanceRooms(request, building_id):
    building = Building.objects.get(building_id=building_id)
    maintenance_rooms = building.rooms.filter(status='maintenance')
    context = {"building":building, "maintenance_rooms":maintenance_rooms}
    return render(request, '', context)

@login_required(login_url='login')
def getRoomDetails(request, room_id):
    room = Room.objects.get(room_id=room_id)
    context = {"room":room}
    return render(request, '', context)

@login_required(login_url='login')
def getRoomsByOwner(request, owner_id):
    rooms = Room.objects.filter(owner__id=owner_id)
    context = {"rooms":rooms, "owner_id":owner_id}
    return render(request, '', context)

@login_required(login_url='login')
def getResidentsByRoom(request, room_id):
    room = Room.objects.get(room_id=room_id)
    residents = room.room_residents.all()
    context = {"room":room, "residents":residents}
    return render(request, '', context)