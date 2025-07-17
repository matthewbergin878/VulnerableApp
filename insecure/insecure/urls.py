from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from insecure.swagger import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]