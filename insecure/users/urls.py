from django.urls import path

from . import views

urlpatterns = [
    path('ssrf/', views.ssrf, name='ssrf'),
    path('internal/', views.internal, name='internal'),
    path('users/', views.users, name="users"),
    path('hello/', views.hello, name="hello")
]