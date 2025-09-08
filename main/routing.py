# main/routing.py
from django.urls import re_path
from core.consumers import InterjectionConsumer

websocket_urlpatterns = [
    re_path(r"ws/interjection/(?P<interjection_id>\d+)/$", InterjectionConsumer.as_asgi()),
]
