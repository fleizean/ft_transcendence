import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from pong.utils import AsyncLockedDict
from django.core.cache import cache
from .utils import add_to_cache, remove_from_cache
#from .models import Game, Tournament, UserProfile
from pong.game import *
import datetime

USER_CHANNEL_NAME = AsyncLockedDict() # key: username, value: channel_name
GAMES = AsyncLockedDict() # key: game_id, value: PongGame object
USER_STATUS = AsyncLockedDict() # key: username, value: game_id or lobby


class PongConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.game_type = self.scope['url_route']['kwargs']['game_type'] # tournament or peer-to-peer or invite
        self.game_id = self.scope['url_route']['kwargs']['game_id'] # game_id or new
        self.user = self.scope['user']

        await self.accept()

        # Add the user to the 'lobby' group
        await self.channel_layer.group_add("lobby", self.channel_name)

        # Set the user's channel name
        await USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        # Add user username to lobby cache
        await USER_STATUS.set(self.user.username, "lobby")
        # Get the list of online users usernames
        lobby_users_usernames = await USER_STATUS.get_keys_with_value('lobby')
        lobby_users_usernames.remove(self.user.username)
        await self.send(text_data=json.dumps({
            'type': 'inlobby',
            'user': self.user.username,
            'users': lobby_users_usernames,
        }))
        await self.channel_layer.group_send("lobby", {
            'type': 'user.inlobby',
            'user': self.user.username,
        })
        if self.game_type == 'tournament':
            await self.tournament_match_handler()
        elif self.game_type == 'invite':
            await self.from_chat_handler()

    async def disconnect(self, close_code):
        game_id = await USER_STATUS.get(self.user.username)
        if game_id != 'lobby':
            game = await GAMES.get(game_id)
            if game != None:
                other_player_channel_name = await USER_CHANNEL_NAME.get(game.otherPlayer(self.user.username))
                await self.record_for_disconnected(game_id, game)
                await self.exit_handler(game_id, game)
                await self.channel_layer.send(other_player_channel_name, {
                    'type': 'game.disconnect',
                    'game_id': game_id,
                    'disconnected': self.user.username,
                    })

        # Remove the user from the 'lobby' group
        await self.channel_layer.group_discard("lobby", self.channel_name)

        # Remove the user's channel name
        await USER_CHANNEL_NAME.delete(self.user.username)

        # Remove user username from lobby cache
        await USER_STATUS.delete(self.user.username)

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
            invitee_username = data.get('invitee_username')
            if matchmaking == 'true':
                invitee_username = await self.matchmaking_handler()
                if invitee_username == None:
                    await self.send(text_data=json.dumps({
                        "error": "No suitable opponent found.",
                    }))
                    return
            if await self.check_is_user_inlobby(invitee_username):                
                invitee_channel_name = await USER_CHANNEL_NAME.get(invitee_username)
                if invitee_channel_name:
                    await self.channel_layer.send(invitee_channel_name, {
                        'type': 'game.invite',
                        'inviter': self.user.username,
                        'invitee': invitee_username,
                    })

        elif action == 'accept':
            inviter_username = data.get('inviter_username')
            await self.accept_handler(inviter_username)

        elif action == 'decline':
            inviter_username = data.get('inviter_username')
            await self.decline_handler(inviter_username)

        
        elif action == 'start.request':
            opponent_username = data.get('opponent')
            game_id = data.get('game_id')
            vote = data.get('vote')
            await self.start_handler(game_id, opponent_username, vote)

        elif action == 'leave.game':
            game_id = data.get('game_id')
            left = data.get('left')
            opponent = data.get('opponent')
            await self.leave_handler(game_id, left, opponent)

        elif action == 'restart': #? not sure is needed or not
            invitee_username = data.get('invitee_username')
            invitee_channel_name = await USER_CHANNEL_NAME.get(invitee_username)
            if invitee_channel_name:
                await self.channel_layer.send(invitee_channel_name, {
                    'type': 'game.restart',
                    'inviter': self.user.username,
                })
        elif action == 'exit':
            game_id = data.get('game_id')
            game = await GAMES.get(game_id)
            if await self.check_is_users_ingame(game_id, game):
                await self.exit_handler(game_id, game)

        #TODO Maybe remove this
        elif action == 'pause.game':
            game_id = data.get('game_id')
            game = await GAMES.get(game_id)
            if (game != None):
                game.pauseGame()
                await self.channel_layer.group_send(
                    game.group_name,
                    {
                        "type": "game.pause",
                        "game_id": game_id,
                    }
                )

        #TODO Maybe remove this
        elif action == 'resume.game':
            game_id = data.get('game_id')
            game = await GAMES.get(game_id)
            if (game != None):
                game.resumeGame()
                await self.channel_layer.group_send(
                    game.group_name,
                    {
                        "type": "game.resume",
                        "game_id": game_id,
                    }
                )

        elif action == "ball": #? Needs validation
                # Make a move in a game and get the ball coordinates
                # we send a message to the clients with the ball coordinates
                game_id = data["game_id"]
                # Move and Get ball coordinates
                game = await GAMES.get(game_id) #? When games status is ended, game_id is deleted from GAMES cache
                if (game != None): #? So game becomes None. Is this check enough? or moving delete to end solve without this
                    if (game.status == Status.PLAYING):
                        x, y, player1_score, player2_score = game.moveBall()
                        # Send a message to the game group with the game id, the move coordinates
                        await self.channel_layer.group_send(
                            game.group_name,
                            {
                                "type": "game.ball",
                                "game_id": game_id,
                                "x": x,
                                "y": y,
                                "player1_score": player1_score,
                                "player2_score": player2_score,
                            }
                        )
                    elif (game.status == Status.ENDED and not game.no_more):
                        await self.end_handler(game_id, game)
                        game.no_more = True

        elif action == "paddle": #? Needs validation
            # Make a move in a game
            game_id = data["game_id"]
            dir = data["direction"]
            # Move and Get paddle coordinate
            game = await GAMES.get(game_id) #? When games status is ended, game_id is deleted from GAMES cache
            if (game != None):  #? So game becomes None. Is this check enough? or moving delete to end solve without this
                y = game.movePaddle(self.user.username, dir)
                # Send a message to the game group with the game id, the paddle coordinate, and the player's username
                await self.channel_layer.group_send(
                    game.group_name,
                    {
                        "type": "game.paddle",
                        "game_id": game_id,
                        "y": y,
                        "player": self.user.username,
                    }
                )
        elif action == "ability":
            game_id = data["game_id"]
            ability = data["abilities"]
            game = await GAMES.get(game_id)
            if (game != None):
                if (game.status == Status.PLAYING):
                    game.activateAbility(self.user.username, ability)
                    await self.channel_layer.group_send(
                        game.group_name,
                        {
                            "type": "game.ability",
                            "game_id": game_id,
                            "player": self.user.username,
                            "ability": ability,
                        }
                    )

    ### HANDLERS ###
    async def tournament_match_handler(self):
        game_id, player1, player2, group_name, tournament_id = await self.match_details()
        if await self.check_is_user_inlobby(player1) and await self.check_is_user_inlobby(player2):
            player1_channel_name = await USER_CHANNEL_NAME.get(player1)
            player2_channel_name = await USER_CHANNEL_NAME.get(player2)

            await self.channel_layer.group_add(group_name, player1_channel_name)
            await self.channel_layer.group_add(group_name, player2_channel_name)

            await GAMES.set(game_id, PongGame(player1, player2, tournament_id))

            await self.channel_layer.group_send(group_name, {
                'type': 'tournament.match',
                'tournament_id': tournament_id,
                'game_id': game_id,
                'player1': player1,
                'player2': player2,
            })
        
    async def from_chat_handler(self):
        game_id, player1, player2, group_name, tournament_id = await self.match_details()
        if await self.check_is_user_inlobby(player1) and await self.check_is_user_inlobby(player2):
            player1_channel_name = await USER_CHANNEL_NAME.get(player1)
            player2_channel_name = await USER_CHANNEL_NAME.get(player2)

            await self.channel_layer.group_add(group_name, player1_channel_name)
            await self.channel_layer.group_add(group_name, player2_channel_name)

            await GAMES.set(game_id, PongGame(player1, player2))

            await self.channel_layer.group_send(group_name, {
                'type': 'chat.game',
                'game_id': game_id,
                'player1': player1,
                'player2': player2,
            })

    async def accept_handler(self, inviter_username):
        inviter_channel_name = await USER_CHANNEL_NAME.get(inviter_username)
        group_name = f"{inviter_username}-{self.user.username}"
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.channel_layer.group_add(group_name, inviter_channel_name)

        # Create a new game instance and save it to the database
        game = await self.create_game(group_name, inviter_username, self.user.username)
        # Create a new game instance and save it to the cache
        await GAMES.set(game.id, PongGame(inviter_username, self.user.username))

        await self.channel_layer.group_send(group_name, {
            'type': 'game.accept',
            'accepter': self.user.username,
            'accepted': inviter_username,
            'game_id': game.id,
        })

    async def decline_handler(self, inviter_username):
        inviter_channel_name = await USER_CHANNEL_NAME.get(inviter_username)
        await self.channel_layer.send(inviter_channel_name, {
            'type': 'game.decline',
            'decliner': self.user.username,
            'declined': inviter_username,
        })

    async def start_handler(self, game_id, opponent_username, vote):
        # Get the current game status and update it with the vote count
        game = await GAMES.get(game_id)
        current = game.status.value + int(vote)
        await GAMES.set_field_value(game_id, Status(current), "status")
        
        # Check both players voted to start the game
        if Status(current) == Status.PLAYING: # both players voted to start the game
            await USER_STATUS.set(self.user.username, game_id)
            await USER_STATUS.set(opponent_username, game_id)
            cache.set(f"playing_{self.user.username}", True)
            cache.set(f"playing_{opponent_username}", True)
            
            """             # Send message to lobby #? Maybe unnecesary bcs playing_username cache
            await self.channel_layer.group_send('lobby', {
                'type': 'users.ingame',
                'game_type': self.game_type,
                'players': [self.user.username, opponent_username],
            }) """
        await self.channel_layer.group_send(game.group_name, {
                'type': 'game.start',
                'game_id': game_id,
                'vote': current,
        })
        
    async def leave_handler(self, game_id, left, opponent):
        # Get scores
        game = await GAMES.get(game_id) 
        left_score = game.getScore(left) # blocking?
        opponent_score = MAX_SCORE # set max score automaticaly
        duration = game.getDuration()
        # Record the game
        await self.record_stats_elo_wallet(game_id, opponent_score, left_score, opponent, left, duration)
        await USER_STATUS.set(game.player1.username, 'lobby') #?
        await USER_STATUS.set(game.player2.username, 'lobby') #?

        await self.channel_layer.group_send(
            game.group_name,
            {
                "type": "game.leave",
                "game_id": game_id,
                "left": self.user.username,
                "left_score": left_score,
                "opponent_score": opponent_score,
                "winner": opponent,
                "loser": left,
            }
        )
        #await self.exit_handler(game_id, game, opponent) #! Invalid channel name error

    async def exit_handler(self, game_id, game):
        # Discard both from the game group
        opponent = game.otherPlayer(self.user.username)
        opponent_channel_name = await USER_CHANNEL_NAME.get(opponent)
        await self.channel_layer.group_discard(game.group_name, self.channel_name)
        await self.channel_layer.group_discard(game.group_name, opponent_channel_name)
        cache.set(f"playing_{self.user.username}", False)
        cache.set(f"playing_{opponent}", False)
        # delete the game from the cache
        await GAMES.delete(game_id)

    async def end_handler(self, game_id, game):
        # Get scores
        player1_score = game.player1.score
        player2_score = game.player2.score
        duration = game.getDuration()
        winner, loser, winner_score, loser_score = game.getWinnerLoserandScores()
        # Set the game winner, scores and save it to the database
        await self.record_stats_elo_wallet(game_id, winner_score, loser_score, winner, loser, duration)
        await USER_STATUS.set(game.player1.username, 'lobby') #?
        await USER_STATUS.set(game.player2.username, 'lobby') #?
        
        #? Maybe unnecesary
        await self.channel_layer.group_send(
            game.group_name,
            {
                "type": "game.end",
                "game_id": game_id,
                "player1_score": player1_score,
                "player2_score": player2_score,
                "winner": winner,
                "loser": loser,
            }
        )


    ## SENDERS ##
    async def user_inlobby(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            'type': 'user.inlobby',
            'user': user,
        }))

    async def user_outlobby(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            'type': 'user.outlobby',
            'user': user,
        }))

    async def game_disconnect(self, event):
        game_id = event['game_id']
        disconnected = event['disconnected']
        await self.send(text_data=json.dumps({
            'type': 'game.disconnect',
            'game_id': game_id,
            'disconnected': disconnected,
        }))

    async def game_invite(self, event):
        inviter = event['inviter']
        invitee = event['invitee']
        await self.send(text_data=json.dumps({
            'type': 'game.invite',
            'inviter': inviter,
            'invitee': invitee,
        }))

    async def tournament_match(self, event):
        tournament_id = event['tournament_id']
        game_id = event['game_id']
        player1 = event['player1']
        player2 = event['player2']
        await self.send(text_data=json.dumps({
            'type': 'tournament.match',
            'tournament_id': tournament_id,
            'game_id': game_id,
            'player1': player1,
            'player2': player2,
        }))

    async def chat_game(self, event):
        game_id = event['game_id']
        player1 = event['player1']
        player2 = event['player2']
        await self.send(text_data=json.dumps({
            'type': 'chat.game',
            'game_id': game_id,
            'player1': player1,
            'player2': player2,
        }))

    async def game_accept(self, event):
        accepter = event['accepter']
        accepted = event['accepted']
        game_id = event['game_id']
        await self.send(text_data=json.dumps({
            'type': 'game.accept',
            'accepter': accepter,
            'accepted': accepted,
            'game_id': game_id,
        }))

    async def game_decline(self, event):
        decliner = event['decliner']
        declined = event['declined']
        await self.send(text_data=json.dumps({
            'type': 'game.decline',
            'decliner': decliner,
            'declined': declined,
        }))

    async def game_start(self, event):
        game_id = event['game_id']
        vote = event['vote']
        await self.send(text_data=json.dumps({
            'type': 'game.start',
            'game_id': game_id,
            'vote': vote,
        }))

    #? Maybe unnecesary
    async def users_ingame(self, event):
        game_type = event['game_type']
        players = event['players']
        await self.send(text_data=json.dumps({
            'type': 'users.ingame',
            'game_type': game_type,
            'players': players,
        }))

    async def game_leave(self, event):
        game_id = event['game_id']
        left = event['left']
        left_score = event['left_score']
        opponent_score = event['opponent_score']
        winner = event['winner']
        loser  = event['loser']
        await self.send(text_data=json.dumps({
            'type': 'game.leave',
            'game_id': game_id,
            'left': left,
            'left_score': left_score,
            'opponent_score': opponent_score,
            'winner': winner,
            'loser': loser,
        }))

    async def game_end(self, event):
        game_id = event['game_id']
        player1_score = event['player1_score']
        player2_score = event['player2_score']
        winner = event['winner']
        loser = event['loser']

        await self.send(text_data=json.dumps({
            'type': 'game.end',
            'game_id': game_id,
            'player1_score': player1_score,
            'player2_score': player2_score,
            'winner': winner,
            'loser': loser,
        }))

    async def game_restart(self, event):
        inviter = event['inviter']
        await self.send(text_data=json.dumps({
            'type': 'game.restart',
            'inviter': inviter,
        }))
        
    async def game_pause(self, event):
        game_id = event['game_id']
        await self.send(text_data=json.dumps({
            'type': 'game.pause',
            'game_id': game_id,
        }))

    async def game_resume(self, event):
        game_id = event['game_id']
        await self.send(text_data=json.dumps({
            'type': 'game.resume',
            'game_id': game_id,
        }))

    async def game_ball(self, event):
        game_id = event['game_id']
        x = event['x']
        y = event['y']
        player1_score = event['player1_score']
        player2_score = event['player2_score']
        await self.send(text_data=json.dumps({
            'type': 'game.ball',
            'game_id': game_id,
            'x': x,
            'y': y,
            'player1_score': player1_score,
            'player2_score': player2_score,
        }))

    async def game_paddle(self, event):
        game_id = event['game_id']
        y = event['y']
        player = event['player']
        await self.send(text_data=json.dumps({
            'type': 'game.paddle',
            'game_id': game_id,
            'y': y,
            'player': player,
        }))

    async def game_ability(self, event):
        game_id = event['game_id']
        player = event['player']
        ability = event['ability']
        await self.send(text_data=json.dumps({
            'type': 'game.ability',
            'game_id': game_id,
            'player': player,
            'ability': ability,
        }))

    # Helper methods to interact with the database #
    async def create_game(self, group_name, player1, player2):
        from .models import Game, UserProfile
        # Create a new game instance with the given players and an group_name
        accepted = await UserProfile.objects.aget(username=player1)
        accepter = await UserProfile.objects.aget(username=player2)           
        game = await Game.objects.acreate(group_name=group_name, player1=accepted, player2=accepter)
        return game
    

    @database_sync_to_async
    def match_details(self):
        from .models import Game
        game = Game.objects.get(id=self.game_id)
        game_id = game.id
        player1 = game.player1.username
        player2 = game.player2.username
        group_name = game.group_name
        tournament_id = game.tournament_id
        return game_id, player1, player2, group_name, tournament_id


    @database_sync_to_async
    def record_stats_elo_wallet(self, game_id, winner_score, loser_score, winner, loser, game_duration):
        from .models import Game, UserProfile
        from .update import update_wallet_elo, update_stats_pong, update_tournament

        game = Game.objects.get(id=game_id)
        if game.winner == None:
            game.winner_score = winner_score
            game.loser_score = loser_score
            game.winner =UserProfile.objects.get(username=winner)
            game.loser = UserProfile.objects.get(username=loser)
            game.game_duration = datetime.timedelta(seconds=game_duration)
            game.save()

            update_wallet_elo(game.winner, game.loser)
            update_stats_pong(game.winner, game.loser, winner_score, loser_score, game_duration, "remote")

            # İf the game is a tournament game
            if game.tournament_id:   #? Check
                update_tournament(game)


    async def record_for_disconnected(self, game_id, game):
        duration = game.getDuration()
        if game.player1.username == self.user.username:
            await self.record_stats_elo_wallet(game_id, game.player1.score, MAX_SCORE, game.player2.username, game.player1.username, duration)
        else:
            await self.record_stats_elo_wallet(game_id, MAX_SCORE, game.player2.score, game.player1.username, game.player2.username, duration)

    async def check_is_user_inlobby(self, username):
        answer = await USER_STATUS.get(username) == 'lobby'
        if not answer:
            await self.send(text_data=json.dumps({
                "error": "User is not in the lobby.",
            }))
        return answer
    
    async def check_is_users_ingame(self, game_id, game):
        answer = await USER_STATUS.get(game.player1.username) == game_id and await USER_STATUS.get(game.player2.username) == game_id
        return answer

    async def matchmaking_handler(self):
        from .models import UserProfile
        # Get the current user's elo_point
        current_user = await UserProfile.objects.aget(username=self.user.username)
        current_user_elo = current_user.elo_point
        # Get a list of online users
        lobby_users_usernames = await USER_STATUS.get_keys_with_value('lobby')
        lobby_users_usernames.remove(self.user.username) #TODO if user not in lobby

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


