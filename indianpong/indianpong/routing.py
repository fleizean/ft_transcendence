from channels.routing import ProtocolTypeRouter, URLRouter
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
)
