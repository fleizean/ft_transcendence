
from django.urls import re_path

from pong import consumers

websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]

