from django.test import TestCase

# Create your tests here.
# FILEPATH: /home/gusto/ft_transcendence_newpdf/indianpong/indianpong/tests.py
import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import reverse
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from pong.consumers import PongConsumer
from indianpong.asgi import application

# Define the application for testing

class TestPongConsumer(TestCase):
    @pytest.mark.asyncio
    async def test_pong_consumer(self):
        # Initialize the WebsocketCommunicator with the testing application and the path
        communicator = WebsocketCommunicator(application, '/ws/pong/')

        # Connect to the websocket
        connected, _ = await communicator.connect()
        assert connected

        # Test sending data
        await communicator.send_json_to({"type": "ping"})
        response = await communicator.receive_json_from()
        assert response['type'] == 'pong'

        # Disconnect
        await communicator.disconnect()