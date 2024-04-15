import datetime
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

        # Get the number of users in the lobby
        lobby_users_usernames = await RPS_USER_STATUS.get_keys_with_value('search')
        lobby_users_count = len(lobby_users_usernames)
        await self.send(text_data=json.dumps({
            'type': 'insearch',
            'user': self.user.username,
            'user_count': lobby_users_count,
        }))

        #? Maybe unnecessary
        await self.channel_layer.group_send("search", {
            'type': 'user.insearch',
            'user': self.user.username,
        })

    async def disconnect(self, close_code):
        game_id = await RPS_USER_STATUS.get(self.user.username)
        if game_id != 'search':
            game = await RPS_GAMES.get(game_id)
            if game != None:
                other_player_channel_name = await RPS_USER_CHANNEL_NAME.get(game.otherPlayer(self.user.username))
                await self.record_for_disconnected(game_id, game)
                await self.exit_handler(game_id, game)
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
            'type': 'user.outsearch',
            'user': self.user.username,
        })

        # Close the websocket connection
        await self.close(close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('type')

        if action == 'matchmaking':
            opponent = await self.matchmaking_handler()
            if opponent == None:
                    await self.send(text_data=json.dumps({
                        "error": "No suitable opponent found.",
                    }))
                    return
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
                await self.channel_layer.group_send(group_name, {
                    'type': 'start',
                    'game_id': game.id,
                    'player1': self.user.username,
                    'player2': opponent,
                })
            else:
                await self.send(text_data=json.dumps({
                    'type': 'matchmaking.notfound',
                }))

        elif action == 'choice':
            game_id = data.get('game_id')
            choice = data.get('choice')
            game = await RPS_GAMES.get(game_id)
            game.play(self.user.username, choice)
            if game.both_played():
                player1_choice, player2_choice = game.getChoices()
                result = game.round_result()
                player1_score, player2_score = game.get_scores()
                await self.channel_layer.group_send(game.group_name, {
                    'type': 'result',
                    'game_id': game_id,
                    'result': result,
                    'player1_choice': player1_choice,
                    'player2_choice': player2_choice,
                    'player1_score': player1_score,
                    'player2_score': player2_score,
                })
                if game.check_is_over():
                    winner, loser, winner_score, loser_score = game.getWinnerLoserandScores()
                    game_duration = game.getDuration()
                    await self.record_stats_elo_wallet(game_id, winner_score, loser_score, winner, loser, game_duration)
                    await self.channel_layer.group_send(game.group_name, {
                        'type': 'result',
                        'game_id': game_id,
                        'result': 'OVER',
                        'player1_choice': player1_choice,
                        'player2_choice': player2_choice,
                        'player1_score': player1_score,
                        'player2_score': player2_score,
                    })


    ### Handlers ###
    async def matchmaking_handler(self):
        from .models import UserProfile
        # Get the current user's elo_point
        current_user = await UserProfile.objects.aget(username=self.user.username)
        current_user_elo = current_user.elo_point
        # Get a list of online users
        lobby_users_usernames = await RPS_USER_STATUS.get_keys_with_value('search')
        lobby_users_usernames.remove(self.user.username) #TODO if user not in search

        return await self.get_similar_users(lobby_users_usernames, current_user_elo)
        

    @database_sync_to_async
    def get_similar_users(self, lobby_users_usernames, current_user_elo):
        from .models import UserProfile
        users = UserProfile.objects.filter(username__in=lobby_users_usernames, elo_point__gte=current_user_elo-100, elo_point__lte=current_user_elo+100).all()
        similar_users = [user.username for user in users]
        if similar_users:
            invitee_username = random.choice(similar_users)
        else:
            invitee_username = random.choice(lobby_users_usernames) if lobby_users_usernames else None
        
        return invitee_username
    
    async def exit_handler(self, game_id, game): 
        # Discard both from the game group
        opponent = game.otherPlayer(self.user.username)
        opponent_channel_name = await RPS_USER_CHANNEL_NAME.get(opponent)
        await self.channel_layer.group_discard(game.group_name, self.channel_name)
        await self.channel_layer.group_discard(game.group_name, opponent_channel_name)
        cache.set(f"playing_{self.user.username}", False)
        cache.set(f"playing_{opponent}", False)
        # delete the game from the cache
        await RPS_GAMES.delete(game_id)
    
    ## Senders ##
    async def user_insearch(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user.insearch',
            'user': event['user'],
        }))

    async def user_outsearch(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user.outsearch',
            'user': event['user'],
        }))

    async def game_disconnect(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game.disconnect',
            'game_id': event['game_id'],
            'disconnected': event['disconnected'],
        }))    
    
    async def result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'result',
            'game_id': event['game_id'],
            'result': event['result'],
            'player1_choice': event['player1_choice'],
            'player2_choice': event['player2_choice'],
            'player1_score': event['player1_score'],
            'player2_score': event['player2_score'],
        }))

    
    
    async def start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'start',
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
    
    @database_sync_to_async
    def record_stats_elo_wallet(self, game_id, winner_score, loser_score, winner, loser, game_duration):
        from .models import Game, UserProfile
        from .update import update_wallet_elo, update_stats_rps

        game = Game.objects.get(id=game_id)
        game.game_kind = "rps"
        game.winner_score = winner_score
        game.loser_score = loser_score
        game.winner =UserProfile.objects.get(username=winner)
        game.loser = UserProfile.objects.get(username=loser)
        game.game_duration = datetime.timedelta(seconds=game_duration)
        game.save()

        update_wallet_elo(game.winner, game.loser)
        update_stats_rps(game.winner, game.loser, winner_score, loser_score, game_duration, "remote")

    async def record_for_disconnected(self, game_id, game):
        duration = game.getDuration()
        if game.shaker1.username == self.user.username:
            await self.record_stats_elo_wallet(game_id, game.shaker1.score, game.max_score, game.shaker2.username, game.shaker1.username, duration)
        else:
            await self.record_stats_elo_wallet(game_id, game.max_score, game.shaker2.score, game.shaker1.username, game.shaker2.username, duration)