
from django.urls import re_path
from django.urls import path

from pong import consumers, consumers2

""" websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<room_name>[\w-]+)/$', consumers.PongConsumer.as_asgi()),
] """

websocket_urlpatterns = [
    path("ws/play/<room_code>/", consumers2.MultiplexerConsumer.as_asgi()),
]