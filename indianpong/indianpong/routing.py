
from django.urls import re_path
from django.urls import path

from pong import consumers, consumer_tournament

websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/tournament/(?P<room_name>[\w-]+)/$', consumer_tournament.TournamentConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<room_name>[\w-]+)/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/rps/$', consumers.RPSConsumer.as_asgi()),
]

