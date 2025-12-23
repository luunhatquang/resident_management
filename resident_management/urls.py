from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from resident_management.core.views import dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Frontend Dashboard
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", dashboard_view, name="home"), # Set làm trang chủ luôn
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]