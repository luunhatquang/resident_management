from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()
router.register(r'api/buildings', views.BuildingViewSet, basename='building')

urlpatterns = [
    path('buildings/', views.getAllBuildings, name='get_all_buildings'),
    path('buildings/filter/<str:name_contains>/', views.getBuildingWithFilter, name='get_building_with_filter'),
    path('buildings/detail/<str:building_id>/', views.getBuildingDetails, name='get_building_details'),
    path('buildings/status/<str:status>/', views.getBuilingsByStatus, name='get_buildings_by_status'),
    path('buildings/<str:building_id>/rooms/', views.getRoomsByBuilding, name='get_rooms_by_building'),
    path('buildings/<str:building_id>/rooms/available/', views.getAvailableRooms, name='get_available_rooms'),
    path('buildings/<str:building_id>/rooms/unavailable/', views.getUnavailableRooms, name='get_unavailable_rooms'),
    path('buildings/<str:building_id>/rooms/maintenance/', views.getMaintenanceRooms, name='get_maintenance_rooms'),
    path('rooms/detail/<str:room_id>/', views.getRoomDetails, name='get_room_details'),
    path('owners/<str:owner_id>/rooms/', views.getRoomsByOwner, name='get_rooms_by_owner'),
    path('rooms/<str:room_id>/residents/', views.getResidentsByRoom, name='get_residents_by_room'),   
    path('rooms/<str:room_id>/update/', views.updateRoom, name='update_room'),  
    path('buildings/<str:building_id>/update/', views.updateBuilding, name='update_building'),
    path('buildings/create/', views.createBuilding, name='create_building'),
    path('rooms/create/', views.createRoom, name='create_room'),
    path('', include(router.urls)),
    
]