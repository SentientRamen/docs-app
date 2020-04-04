from django.contrib import admin
from django.urls import path, include

from docs.views import login_page


# The `urlpatterns` list routes URLs to views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('docs.urls')),
    path('', login_page),
]
