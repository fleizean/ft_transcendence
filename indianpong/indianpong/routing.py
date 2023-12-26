
from django.urls import re_path

from pong import consumers

websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
]




""" from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from pong.consumers import ChatConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/chat/", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
) """