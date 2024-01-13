import json
import math
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the player to the game (e.g., assign a unique player ID)
        player_id = self.scope['user'].id  # Assuming user authentication is enabled
        await self.send(text_data=json.dumps({'type': 'connect', 'player_id': player_id}))

        # Broadcast to other players that a new player has connected
        await self.channel_layer.group_add("pong_game", self.channel_name)
        await self.channel_layer.group_send("pong_game", {'type': 'player_update', 'player_id': player_id})

    async def disconnect(self, close_code):
        # Remove the player from the game
        player_id = self.scope['user'].id
        await self.channel_layer.group_discard("pong_game", self.channel_name)

        # Broadcast to other players that a player has disconnected
        await self.channel_layer.group_send("pong_game", {'type': 'player_disconnect', 'player_id': player_id})

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'move_paddle':
            # Handle paddle movement logic (update player's paddle position)
            # For example, you might update the player's paddle position based on data['direction']
            # Broadcast the updated paddle position to all connected clients
            player_id = self.scope['user'].id
            await self.channel_layer.group_send("pong_game", {'type': 'paddle_update', 'player_id': player_id, 'position': data['position']})

        elif data['type'] == 'start_game':
            # Start the game and initialize the ball
            await self.channel_layer.group_send("pong_game", {'type': 'start_game'})

        elif data['type'] == 'ball_update':
            # Handle ball movement logic (update ball position)
            # For example, you might update the ball position based on data['ball']
            # Broadcast the updated ball position to all connected clients
            await self.channel_layer.group_send("pong_game", {'type': 'ball_update', 'ball': data['ball']})

    async def player_update(self, event):
        await self.send(text_data=json.dumps({'type': 'player_update', 'player_id': event['player_id']}))

    async def player_disconnect(self, event):
        await self.send(text_data=json.dumps({'type': 'player_disconnect', 'player_id': event['player_id']}))

    async def paddle_update(self, event):
        await self.send(text_data=json.dumps({'type': 'paddle_update', 'player_id': event['player_id'], 'position': event['position']}))

    async def start_game(self, event):
        # Initialize the ball position and velocity
        ball = {'x': 400, 'y': 300, 'speed': 5, 'dx': random.choice([1, -1]), 'dy': random.uniform(-1, 1)}
        await self.channel_layer.group_send("pong_game", {'type': 'ball_update', 'ball': ball})

    async def ball_update(self, event):
        ball = event['ball']

        # Update the ball position based on its velocity and direction
        ball['x'] += ball['speed'] * ball['dx']
        ball['y'] += ball['speed'] * ball['dy']

        # Check for collisions with paddles and walls (adjust the logic based on your game)
        # For simplicity, this example assumes a basic collision with top/bottom walls only
        if ball['y'] <= 0 or ball['y'] >= 600:
            ball['dy'] = -ball['dy']

        # Broadcast the updated ball position to all connected clients
        await self.channel_layer.group_send("pong_game", {'type': 'ball_update', 'ball': ball})

