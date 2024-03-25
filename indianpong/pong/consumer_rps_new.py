import json
import random
from channels.db import database_sync_to_async
from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import AsyncLockedDict
from .rps import *

RPS_USER_CHANNEL_NAME = AsyncLockedDict() # key: username, value: channel_name
RPS_GAMES = AsyncLockedDict() # key: game_id, value: RPSGame object
RPS_USER_STATUS = AsyncLockedDict() # key: username, value: game_id or search


class RPSConsumer(AsyncWebsocketConsumer):
        
    async def connect(self):
        self.user = self.scope['user']

        await self.accept()

        # Add the user to the 'lobby' group
        await self.channel_layer.group_add("search", self.channel_name)

        # Set the user's channel name
        await RPS_USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        # Add user username to lobby cache
        await RPS_USER_STATUS.set(self.user.username, "search")
        #? Maybe unnecessary
        await self.channel_layer.group_send("search", {
            'type': 'user.inlobby',
            'user': self.user.username,
        })

    async def disconnect(self, close_code):
        game_id = await RPS_USER_STATUS.get(self.user.username)
        if game_id != 'search':
            game = await RPS_GAMES.get(game_id)
            await self.record_for_disconnected(game_id, game)
            await self.exit_handler(game_id, game, game.otherPlayer(self.user.username))
            other_player_channel_name = await RPS_USER_CHANNEL_NAME.get(game.otherPlayer(self.user.username))
            await self.channel_layer.send(other_player_channel_name, {
                'type': 'game.disconnect',
                'game_id': game_id,
                'disconnected': self.user.username,
                })

        # Remove the user from the 'lobby' group
        await self.channel_layer.group_discard("search", self.channel_name)

        # Remove the user's channel name
        await RPS_USER_CHANNEL_NAME.delete(self.user.username)

        # Remove user username from lobby cache
        await RPS_USER_STATUS.delete(self.user.username)

        #? Maybe unnecessary
        # Set the user's status to offline
        await self.channel_layer.group_send("search", {
            'type': 'user.outlobby',
            'user': self.user.username,
        })

        # Close the websocket connection
        await self.close(close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'matchmaking':
            opponent = await self.matchmaking_handler()
            if opponent:
                # Get the channel name of the shaker
                opponent_channel_name = await RPS_USER_CHANNEL_NAME.get(opponent)
                group_name = f'rps_{self.user.username}_{opponent}'
                # Create a new game instance in database
                game = await self.create_game(group_name, self.user.username, opponent)
                # Add both players to the group
                await self.channel_layer.group_add(group_name, self.channel_name)
                await self.channel_layer.group_add(group_name, opponent_channel_name)
                # Save the game instance in the cache
                await RPS_GAMES.set(game.id, RPS(self.user.username, opponent))
                # Set the user's status to playing
                await RPS_USER_STATUS.set(self.user.username, game.id)
                await RPS_USER_STATUS.set(opponent, game.id)
                cache.set(f"playing_{self.user.username}", True)
                cache.set(f"playing_{opponent}", True)

                # Send the game id to both players
                await self.channel_layer.send(group_name, {
                    'type': 'game.start',
                    'game_id': game.id,
                    'player1': self.user.username,
                    'player2': opponent,
                })
            else:
                await self.send(text_data=json.dumps({
                    'type': 'matchmaking.error',
                    'message': 'No opponent found',
                }))

        elif action == 'choice':
            await self.choice_handler(data)
        elif action == 'restart':
            await self.restart_handler(data)
        elif action == 'exit':
            await self.exit_handler()

    ### Handlers ###
    async def matchmaking_handler(self):
        from .models import UserProfile
        # Get the current user's elo_point
        current_user_elo = await UserProfile.objects.aget(username=self.user.username).elo_point
        
        # Get a list of online users
        lobby_users_usernames = await RPS_USER_STATUS.get_keys_with_value('search')
        lobby_users_usernames.remove(self.user.username) #TODO if user not in lobby
        
        # Filter users based on elo_point similarity
        users = await UserProfile.objects.filter(username__in=users, elo_point__gte=current_user_elo-100, elo_point__lte=current_user_elo+100).aall()
        similar_users = [user.username for user in users]
        
        if similar_users:
            opponent = random.choice(similar_users)
        else:
            opponent = random.choice(lobby_users_usernames) #TODO if list is empty
        
        return opponent
    
    ## Senders ##
    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game.start',
            'game_id': event['game_id'],
            'player1': event['player1'],
            'player2': event['player2'],
        }))
    
    # Helpers #
    async def create_game(self,group_name, player1, player2):
        from .models import Game, UserProfile
        # Create a new game instance with the given players and an group_name
        player1 = await UserProfile.objects.aget(username=player1)
        player2 = await UserProfile.objects.aget(username=player2)           
        game = await Game.objects.acreate(game_kind="rps", group_name=group_name, player1=player1, player2=player2)
        return game


