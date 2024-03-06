import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from pong.utils import AsyncLockedDict
from django.core.cache import cache
from .utils import add_to_cache, remove_from_cache
from .models import Game, Tournament, UserProfile, Room, Message#Match, Score, chat
from pong.game import *

USER_CHANNEL_NAME = AsyncLockedDict() # key: id, value: channel_name
GAMES = AsyncLockedDict() # key: game_id, value: PongGame object
#USER_STATUS = AsyncLockedDict() # key: username, value: game_id or online


class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_type = self.scope['url_route']['kwargs']['game_type'] # tournament or peer-to-peer
        self.game_id = self.scope['url_route']['kwargs']['game_id'] # new or game_id
        self.user = self.scope['user']


        await self.accept()

        # Add the user to the 'lobby' group
        await self.channel_layer.group_add("lobby", self.channel_name)

        # Set the user's channel name
        await USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        # Add user username to lobby cache
        add_to_cache('lobby_users', set(), self.user.username)
        # Get the list of online users usernames
        lobby_users_usernames = cache.get('lobby_users', set())

        await self.send(text_data=json.dumps({
            'type': 'inlobby',
            'user': self.user.username,
            'users': lobby_users_usernames,
        }))
        await self.channel_layer.group_send("lobby", {
            'type': 'user.inlobby',
            'user': self.user.username,
        })

    async def disconnect(self, close_code):
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("lobby", self.channel_name)

        # Remove the user's channel name
        await USER_CHANNEL_NAME.delete(self.user.username)

        # Remove user username from lobby cache
        remove_from_cache('lobby_users', set(), self.user.username)

        # Set the user's status to offline
        await self.channel_layer.group_send("lobby", {
            'type': 'user.outlobby',
            'user': self.user.username,
        })

        # Close the websocket connection
        await self.close(close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'invite':
            matchmaking = data.get('matchmaking')
            if matchmaking == 'true':
                # Get a list of online users
                lobby_users_usernames = cache.get('lobby_users', set())
                #Choose from set except the user who sent the invite
                choices = list(lobby_users_usernames)
                choices.remove(self.user.username)
                invitee_username = random.choice(choices)
            else:
                invitee_username = data.get('invitee_username')
                
            invitee_channel_name = await USER_CHANNEL_NAME.get(invitee_username)
            if invitee_channel_name:
                await self.channel_layer.send(invitee_channel_name, {
                    'type': 'game.invite',
                    'inviter': self.user.username,
                })

        elif action == 'accept':
            inviter_username = data.get('inviter_username')
            inviter_channel_name = await USER_CHANNEL_NAME.get(inviter_username)
            if inviter_channel_name:
                group_name = f"{inviter_username}_{self.user.username}"
                await self.channel_layer.group_add(group_name, self.channel_name)
                await self.channel_layer.group_add(group_name, inviter_channel_name)

                # Create a new game instance and save it to the database
                game = await self.create_game(group_name, inviter_username, self.user.username)
                # Create a new game instance and save it to the cache
                await GAMES.set(game.id, PongGame(inviter_username, self.user.username, group_name, game.id))

                await self.channel_layer.send(inviter_channel_name, {
                    'type': 'game.accept',
                    'accepter': self.user.username,
                    'game_id': game.id,
                })

        elif action == 'decline':
            inviter_username = data.get('inviter_username')
            inviter_channel_name = await USER_CHANNEL_NAME.get(inviter_username)
            if inviter_channel_name:
                await self.channel_layer.send(inviter_channel_name, {
                    'type': 'game.decline',
                    'decliner': self.user.username,
                })
        
        elif action == 'start.request':
            opponent_username = data.get('opponent')
            game_id = data.get('game_id')
            vote = data.get('vote')
            # Get the current game status and update it with the vote count
            game = await GAMES.get(game_id)
            current = game.status.value + int(vote)
            await GAMES.set_field_value(game_id, Status(current), "status")
            
            # Check both players voted to start the game
            if Status(current) == Status.STARTED: # both players voted to start the game
                add_to_cache('playing_users', set(), self.user.username)
                add_to_cache('playing_users', set(), opponent_username)
                # Send message to lobby
                await self.channel_layer.group_send('lobby', {
                    'type': 'users.ingame',
                    'game_type': self.game_type,
                    'players': [self.user.username, opponent_username],
                })
            await self.channel_layer.group_send(game.group_name, {
                    'type': 'game.start',
                    'game_id': game_id,
                    'vote': current,
            })
        elif action == 'leave.game':
            game_id = data.get('game_id')
            left = data.get('left')
            opponent = data.get('opponent')
            await self.leave_handler(game_id, left, opponent)



        

