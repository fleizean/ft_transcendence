
from django.urls import re_path
from django.urls import path

from pong import consumer_pong, consumer_rps, consumer_status

websocket_urlpatterns = [
    path('ws/online_status/', consumer_status.OnlineStatusConsumer.as_asgi()),
    #re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/remote-game/(?P<game_type>[-\w]+)/(?P<game_id>[\w-]+)/$', consumer_pong.PongConsumer.as_asgi()),
    #re_path(r'^ws/chat/(?P<room_name>[\w-]+)/$', consumers.PongConsumer.as_asgi()),
    re_path(r'^ws/rps/$', consumer_rps.RPSConsumer.as_asgi()),
]

channel_routing = {
    'player.matched': consumer_rps.RPSConsumer.player_matched,
}