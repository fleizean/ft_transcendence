# consumers.py
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, Tournament, UserProfile, Room, Message
from pong.game import *
from pong.tournament import *
from pong.utils import AsyncLockedDict
import json


USER_CHANNEL_NAME = AsyncLockedDict() # key: username, value: channel_name
USER_STATUS = AsyncLockedDict() # key: username, value: game_id or online
GAMES = AsyncLockedDict() # key: game_id, value: PongGame object
TOURNAMENTS = AsyncLockedDict() # key: tournament_id, value: Tournament object
MAX_PLAYERS = 8

class GameConsumer(AsyncJsonWebsocketConsumer):
    # Sub-consumer for game application
    async def game_message(self, event):
        # Handle game messages
        message = event["message"]
        # Do something with the message
        # ...

        # Send a response to the client
        await self.send_json({
            "stream": "game",
            "type": "game.message",
            "message": message,
        })

class ChatConsumer(AsyncJsonWebsocketConsumer):
    # Sub-consumer for chat application
    async def chat_message(self, event):
        # Handle chat messages
        message = event["message"]
        # Do something with the message
        # ...

        # Send a response to the client
        await self.send_json({
            "stream": "chat",
            "type": "chat.message",
            "message": message,
        })

class MultiplexerConsumer(AsyncJsonWebsocketConsumer):
    # Main consumer that multiplexes messages to sub-consumers
    async def connect(self):
        # Get the user from the scope
        self.user = self.scope["user"]
        self.room_group_name = None
        # Check if the user is authenticated
        if self.user.is_anonymous:
            # Reject the connection
            await self.close()

        # Set the user's channel name
        await USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        # Accept the websocket connection
        await self.accept()
        # Add the user to the 'online' group
        await self.channel_layer.group_add("online", self.channel_name)

        # Create sub-consumers and store them in a dict
        self.sub_consumers = {
            "game": GameConsumer(self.scope),
            "chat": ChatConsumer(self.scope),
        }

        # Initialize the sub-consumers
        for consumer in self.sub_consumers.values():
            await consumer.websocket_connect(self.scope)

        # Check if the user is in a game
        game_id = await USER_STATUS.get(self.user.username)
        if game_id != 'online' and game_id != None:
            # Get the game from the cache
            game = await GAMES.get(game_id)
            other_player = game.otherPlayer(self.user.username)
            # Check if the game is paused and the other player is still in game
            if game.status == Status.PAUSED and await USER_STATUS.get(other_player) == game_id:
                await USER_STATUS.set(self.user.username, game_id)
                # Add the user to the game group
                await self.channel_layer.group_add(game.group_name, self.channel_name)
                self.room_group_name = game.group_name
                # Change the game status to 'started'
                game.status = Status.STARTED
                # Send the reconneted message to the other player
                await self.channel_layer.group_send(
                    game.group_name,
                    {
                        "stream": "game",
                        "type": "user.reconnected",
                        "username": self.user.username,
                    }
                )
        else:
            # Set the user's status to 'online'
            await USER_STATUS.set(self.user.username, 'online')


        # Send a message to the group with the user's username
        online_users = await USER_STATUS.get_keys_with_value('online')
        # Send the message to the 'online' group for each stream
        for stream in ["game", "chat"]:
            await self.channel_layer.group_send(
                "online",
                {
                    "stream": stream,
                    "type": "user.online",
                    "username": self.user.username,
                    "users": online_users,
                }
            )
    async def disconnect(self, code):
        # Remove the user from USER_CHANNEL_NAME and USER_STATUS
        await USER_CHANNEL_NAME.delete(self.user.username)
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("online", self.channel_name)
        # Remove the user from the game group
        if self.room_group_name != None:
            # Leave room group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Close the websocket connection
        await self.close()

        # Close the sub-consumers
        for consumer in self.sub_consumers.values():
            await consumer.websocket_disconnect(self.scope)
        
        ###

        game_id = await USER_STATUS.get(self.user.username)
        if game_id != 'online' and game_id != None:
            game = await GAMES.get(game_id)
            #Send opponent a message that the user has disconnected
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "stream": "game",
                    "type": "user.disconnected",
                    "username": self.user.username,
                }
            )
            if game.status == Status.STARTED: # 2 means game is started
                # Pause the game
                game.status = Status.PAUSED #game.pauseGame() #??? implement maybe this
                # Wait 10 seconds for the other player to reconnect
                await asyncio.sleep(10)
                # Check if the player has reconnected if not, record the game as disconnected
                if await USER_STATUS.get(self.user.username) != game_id:
                    # Record the game as disconnected
                    await self.record_for_disconnected(game_id, game)
                    # Delete game cache
                    await GAMES.delete(game_id)
                    # Remove both users from the game group
                    player1_channel_name = await USER_CHANNEL_NAME.get(game.player1.username)
                    player2_channel_name = await USER_CHANNEL_NAME.get(game.player2.username)
                    await self.channel_layer.group_discard(game.group_name, player1_channel_name)
                    await self.channel_layer.group_discard(game.group_name, player2_channel_name)
                    await USER_STATUS.delete(self.user.username)
        else:
            await USER_STATUS.delete(self.user.username)

        # Send the message to the 'online' group for each stream
        for stream in ["game", "chat"]:
            await self.channel_layer.group_send(
                "online",
                {
                    "stream": stream,
                    "type": "user.offline",
                    "username": self.user.username,
                } 
            )

    async def receive_json(self, content):
        # Receive a JSON message from the client
        # Get the stream name and the message type from the content
        stream = content.get("stream")
        type = content.get("type")

        # Route the message to the corresponding sub-consumer
        if stream in self.sub_consumers:
            consumer = self.sub_consumers[stream]
            # Call the handler method on the sub-consumer
            await consumer.dispatch(type, content)
        else:
            # Invalid stream name
            raise ValueError(f"Invalid stream name: {stream}")
