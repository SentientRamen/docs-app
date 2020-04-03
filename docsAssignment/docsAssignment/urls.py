from django.contrib import admin
from django.urls import path, include


# The `urlpatterns` list routes URLs to views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('docs.urls')),

]
