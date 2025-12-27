from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from resident_manage.core.views import dashboard_view, logout_view, room_detail_api
from resident_manage.apps.contract.views import (
    contracts_view, contract_create_view, 
    contract_edit_view, contract_detail_view, 
    contract_delete_view
)
from resident_manage.apps.resident.views import (residents_view, resident_create_view, resident_detail_view,
resident_edit_view, resident_delete_view)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("accounts/", include("resident_manage.apps.accounts.urls")),  
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    
    path("api/room-detail/<int:room_id>/", room_detail_api, name="room_detail_api"),
    
    path("", dashboard_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    
    path("contracts/", contracts_view, name="contracts"),
    path("contracts/add/", contract_create_view, name="contract_add"),
    path("contracts/<int:pk>/", contract_detail_view, name="contract_detail"),
    path("contracts/<int:pk>/edit/", contract_edit_view, name="contract_edit"),
    path("contracts/<int:pk>/delete/", contract_delete_view, name="contract_delete"),
    
    path("residents/", residents_view, name="residents"),
    path('residents/add/', resident_create_view, name='resident_create'),
    path('residents/<int:pk>/', resident_detail_view, name='resident_detail'),
    path('residents/<int:pk>/edit/', resident_edit_view, name='resident_edit'),
    path('residents/<int:pk>/delete/', resident_delete_view, name='resident_delete'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)