from django.urls import path
from . import views

# The `urlpatterns` list routes URLs to views
urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('', views.dashboard, name="dashboard"),
    path('<str:room_name>/', views.room, name='room'),
]