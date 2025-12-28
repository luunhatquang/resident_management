from django.urls import path
from . import views

urlpatterns = [
    path('', views.residents_view, name='residents'),
    path('add/', views.resident_create_view, name='resident_create'),
    path('<int:pk>/', views.resident_detail_view, name='resident_detail'),
    path('<int:pk>/edit/', views.resident_edit_view, name='resident_edit'),
    path('<int:pk>/delete/', views.resident_delete_view, name='resident_delete'),
]

