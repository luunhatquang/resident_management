from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.get_all_expenses, name='get_all_expenses'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/', views.view_expense, name='view_expense'),
    path('expenses/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
]
