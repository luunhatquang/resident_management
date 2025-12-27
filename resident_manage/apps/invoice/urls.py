from django.urls import path
from . import views

urlpatterns = [
    path('invoices/', views.getAllInvoices, name='get_all_invoices'),
    path('invoices/create/', views.create_invoice, name='create_invoice'),
    path('invoices/<str:invoice_id>/', views.getInvoiceDetails, name='get_invoice_details'),
    path('invoices/<str:invoice_id>/update/', views.update_invoice, name='update_invoice'),
    path('invoices/<str:invoice_id>/delete/', views.deleteInvoice, name='delete_invoice'),
    path('invoices/<str:invoice_id>/pay/', views.markAsPaid, name='mark_invoice_paid'),
    path('api/contract/<int:contract_id>/', views.get_contract_details, name='get_contract_details'),
]