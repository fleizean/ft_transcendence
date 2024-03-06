
from django.urls import re_path
from django.urls import path

from pong import consumers, consumer_rps

websocket_urlpatterns = [
    #re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/pong/(?P<game_type>\w+)/(?P<game_id>[\w-]+)/$', consumers.PongConsumer.as_asgi()),
    #re_path(r'^ws/chat/(?P<room_name>[\w-]+)/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/rps/$', consumer_rps.RPSConsumer.as_asgi()),
]

