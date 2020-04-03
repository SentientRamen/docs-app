# docs/routing.py
from django.urls import re_path
from . import consumers

# Route websocket to channel layer
websocket_urlpatterns = [
    re_path(r'ws/docs/(?P<room_name>\w+)/$', consumers.DocConsumer),
]
