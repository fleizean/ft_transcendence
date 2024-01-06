import json
from uuid import uuid4
from asgiref.sync import sync_to_async
import threading
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, Tournament, MatchRecord, UserProfile #Match, Score
from datetime import datetime
from django.db.models import Q

# This is a thread-safe dictionary that can be used to store online status of users
# It is used to check if a user is online before inviting them to a game
# It is also used to get a list of online users to send to the client
# if you use redis-cache you can use it instead of this, redis already recommended for channels
# from django.core.cache import cache
# user_status = cache.get('user_status', {})
# user_status['username'] = 'online'
# cache.set('user_status', user_status)
# online_users = [k for k, v in user_status.items() if v == 'online']

class ThreadSafeDict:
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    @sync_to_async
    def get(self, key, default=None):
        with self.lock:
            return self.dict.get(key, default)

    @sync_to_async
    def set(self, key, value):
        with self.lock:
            self.dict[key] = value

    @sync_to_async
    def delete(self, key):
        with self.lock:
            if key in self.dict:
                del self.dict[key]

    @sync_to_async
    def get_keys_with_value(self, value):
        with self.lock:
            return [k for k, v in self.dict.items() if v == value]
        
USER_STATUS = ThreadSafeDict() # key: username, value: online/playing
USER_CHANNEL_NAME = ThreadSafeDict() # key: username, value: channel_name
GAME_STATUS = ThreadSafeDict()  # key: game_id, value: accepted/started/ended


class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope
        self.user = self.scope["user"]
        # Check if the user is authenticated
        if self.user.is_anonymous:
            # Reject the connection
            await self.close()
        # Set the user's channel name
        USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        #self.user.channel_name = self.channel_name
        #await self.user.asave()
        # Accept the connection
        await self.accept()
        # Add the user to the 'online' group
        await self.channel_layer.group_add("online", self.channel_name)
        # Set the user's status to 'online'
        USER_STATUS.set(self.user.username, 'online')
        # Send a message to the group with the user's username
        online_users = await USER_STATUS.get_keys_with_value('online')
        await self.channel_layer.group_send(
            "online",
            {
                "type": "user.online",
                "username": self.user.username,
                "users": online_users,
            }
        )

    async def disconnect(self, close_code):
        # Remove the user's channel name
        USER_CHANNEL_NAME.delete(self.user.username)
        #self.user.channel_name = None
        USER_STATUS.delete(self.user.username)
        #self.user.online = "offline"
        #await self.user.asave()
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("online", self.channel_name)
        # TODO: Move this to game leave also implement same for tournament
        # Check if user's username is in any game and that game is not ended
        # If so, end the game and record it
        game = await Game.objects.filter(Q(player1=self.user) | Q(player2=self.user), status="started").afirst()
        if game:
            if game.player1 == self.user:
                await self.record_game(game.id, 0, 20, game.player2.username)
            else:
                await self.record_game(game.id, 20, 0, game.player1.username)
            await self.channel_layer.group_discard(game.group_name, self.channel_name)
        # Send a message to the group with the user's username and online users list
        #online_users = await USER_STATUS.get_keys_with_value('online')
        #online_users = await self.get_online_users_list()
        await self.channel_layer.group_send(
            "online",
            {
                "type": "user.offline",
                "username": self.user.username,
                #"users": online_users,
            }
        )

    async def receive(self, text_data):
        # Receive a message from the client
        data = json.loads(text_data)
        action = data["action"]
        if action == "invite":
            # Invite another user to play a game
            invited = data["invited"]
            # TODO: Remove this check after implementing inviting users from online users list with a button
            # Check if the opponent exists
            if not await self.is_user_exist(invited):
                # Send a message to the client with the error
                await self.send(text_data=json.dumps({
                    "error": "User does not exist",
                }))
                return
            #Check if the opponent is online
            if not await self.is_user_online(invited):
                # Send a message to the client with the error
                await self.send(text_data=json.dumps({
                    "error": "User is offline or already playing",
                }))
                return
            # Get the invited channel name
            invited_channel_name = USER_CHANNEL_NAME.get(invited)
            # Set game group name
            group_name = str(uuid4())
            # Add both users to the game group
            await self.channel_layer.group_add(group_name, self.user.channel_name)
            await self.channel_layer.group_add(group_name, invited_channel_name)
            # Send a message to the opponent with the invitation
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "game.invite",
                    "group_name": group_name,
                    "inviter": self.user.username,
                    "invited": invited,
                }
            )
        elif action == "accept":
            # Accept an invitation to play a game
            group_name = data["group_name"]
            accepted = await UserProfile.objects.aget(username=data["accepted"])
            accepter = await UserProfile.objects.aget(username=data["accepter"])

            # Create a new game instance and save it to the database
            game = await self.create_game(group_name, accepted, accepter)
            # Set the game status to 'accepted'
            GAME_STATUS.set(game.id, 'accepted') # maybe key should be group_name
            # Send a message to the game group with the game id and the players' usernames
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.accept",
                    "game_id": game.id,
                    "accepter": accepter.username,
                    "accepted": accepted.username,
                }
            )
        elif action == "decline":
            # Decline an invitation to play a game
            group_name = data["group_name"]
            declined = data["declined"]
            decliner = data["decliner"]
            declined_channel_name = USER_CHANNEL_NAME.get(declined)
            # Get the opponent's user instance from the database
            declined = await UserProfile.objects.aget(username=declined)
            # Send a message to the game group with the game id
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "game.decline",
                    "decliner": decliner,
                    "declined": declined.username,
                }
            )
            # Discard both from the game group
            await self.channel_layer.group_discard(group_name, self.channel_name)
            await self.channel_layer.group_discard(group_name, declined_channel_name)
        elif action == "game.start":
            # Start a game
            game_id = data["game_id"]
            player1 = data["player1"]
            player2 = data["player2"]
            vote_count = data["vote_count"]
            # Get the game instance from the database
            game = await Game.objects.aget(id=game_id)
            # Get the players' user instances from the database
            player1 = await UserProfile.objects.aget(username=player1)
            player2 = await UserProfile.objects.aget(username=player2)
            # Check both players voted to start the game
            if vote_count == 2:
                # Update the players' status to 'playing' and save them to the database
                player1.status = "playing"
                player2.status = "playing"
                await player1.asave()
                await player2.asave()
                # Update the game status to 'started' and save it to the database
                game.status = "started"
                await game.asave()
                # Send a message to the game group with the game id
                await self.channel_layer.group_send(
                    game.group_name,
                    {
                        "type": "game.start",
                        "game_id": game.id,
                        "player1": player1.username,
                        "player2": player2.username,
                        "vote_count": vote_count,
                    }
                )
        elif action == "game.leave":
            pass
        elif action == "ball":
            # Make a move in a game
            game_id = data["game_id"]
            x = data["ballX"]
            y = data["ballY"]
            # Get the game instance from the database
            #game = await self.get_game(game_id)
            #await self.save_game(game)
            # Send a message to the game group with the game id, the move coordinates
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.ball",
                    "game_id": game_id,
                    "ballX": x,
                    "ballY": y,
                }
            )
        elif action == "paddle":
            # Make a move in a game
            game_id = data["game_id"]
            y = data["y"]
            # Get the game instance from the database
            #game = await self.get_game(game_id)
            # Update the game state with the move and save it to the database
            #game.state[x][y] = self.user.username
            #await self.save_game(game)
            # Send a message to the game group with the game id, the move coordinates, and the player's username
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.paddle",
                    "game_id": game_id,
                    "y": y,
                    "player": self.user.username,
                }
            )
        elif action == "end":
            # End a game
            game_id = data["game_id"]
            player1_score = data["player1_score"]
            player2_score = data["player2_score"]
            game = await Game.objects.aget(id=game_id)
            winner = player1_score > player2_score and game.player1.username or game.player2.username
            # Set the game status to 'ended' and save it to the database
            # Set the game winner, scores and save it to the database
            await self.record_game(game_id, player1_score, player2_score, winner)
            # Send a message to the game group with the game id and the winner's username
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.end",
                    "game_id": game_id,
                    "player1_score": player1_score,
                    "player2_score": player2_score,
                    "winner": winner,
                }
            )
    '''
        elif action == "create":
            # Create a new tournament
            name = data["name"]
            #start_date = data["start_date"]
            #end_date = data["end_date"]
            # Create a new tournament instance with the given details and save it to the database
            tournament = await self.create_tournament(name)
            # Send a message to the 'online' group with the tournament id and the tournament details
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.create",
                    "tournament_id": tournament.id,
                    "name": tournament.name,
                    "start_date": tournament.start_date,
                    #"end_date": tournament.end_date,
                }
            )
        elif action == "join":
            # Join a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await self.get_tournament(tournament_id)
            # Add the user to the tournament players and save it to the database
            tournament.participants.add(self.user)
            await self.save_tournament(tournament)
            # Send a message to the 'online' group with the tournament id and the user's username
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.join",
                    "tournament_id": tournament.id,
                    "username": self.user.username,
                }
            )
        elif action == "leave":
            # Leave a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await self.get_tournament(tournament_id)
            # Remove the user from the tournament players and save it to the database
            tournament.participants.remove(self.user)
            await self.save_tournament(tournament)
            # Send a message to the 'online' group with the tournament id and the user's username
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.leave",
                    "tournament_id": tournament.id,
                    "username": self.user.username,
                }
            )
        elif action == "cancel":
            # Cancel a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await self.get_tournament(tournament_id)
            # Delete the tournament instance from the database
            await tournament.delete()
            # Send a message to the 'online' group with the tournament id
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.cancel",
                    "tournament_id": tournament.id,
                }
            )
        elif action == "start":
            # Start a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await self.get_tournament(tournament_id)
            # Update the tournament status to 'started' and save it to the database
            tournament.status = "started"
            await self.save_tournament(tournament)
            # Create the first round of matches and save them to the database
            matches = await self.create_matches(tournament)
            # Send a message to the 'online' group with the tournament id and the matches details
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.start",
                    "tournament_id": tournament.id,
                    "matches": [
                        {
                            "match_id": match.id,
                            "player1": match.player1.username,
                            "player2": match.player2.username,
                        }
                        for match in matches
                    ],
                }
            )
        elif action == "finish":
            # Finish a match in a tournament
            tournament_id = data["tournament_id"]
            match_id = data["match_id"]
            winner = data["winner"]
            # Get the match instance from the database
            match = await self.get_match(match_id)
            # Update the match status to 'finished' and save it to the database
            match.status = "finished"
            await self.save_match(match)
            # Update the tournament standings with the match result and save it to the database
            tournament = await self.get_tournament(tournament_id)
            tournament.standings[winner] += 1
            await self.save_tournament(tournament)
            # Send a message to the 'online' group with the match id and the winner's username
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.finish",
                    "match_id": match.id,
                    "winner": winner,
                }
            )
        elif action == "next":
            # Start the next round of matches in a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await self.get_tournament(tournament_id)
            # Check if the tournament is over
            if len(tournament.standings) == 1:
                # Update the tournament status to 'ended' and save it to the database
                tournament.status = "ended"
                await self.save_tournament(tournament)
                # Send a message to the 'online' group with the tournament id and the winner's username
                await self.channel_layer.group_send(
                    "online",
                    {
                        "type": "tournament.end",
                        "tournament_id": tournament.id,
                        "winner": list(tournament.standings.keys())[0],
                    }
                )
            else:
                # Create the next round of matches and save them to the database
                matches = await self.create_matches(tournament)
                # Send a message to the 'online' group with the tournament id and the matches details
                await self.channel_layer.group_send(
                    "online",
                    {
                        "type": "tournament.next",
                        "tournament_id": tournament.id,
                        "matches": [
                            {
                                "match_id": match.id,
                                "player1": match.player1.username,
                                "player2": match.player2.username,
                            }
                            for match in matches
                        ],
                    }
                )
    '''
    # Helper methods to interact with the database
    @database_sync_to_async
    def create_game(self, group_name, player1, player2):
        # Create a new game instance with the given players and an group_name
        game = Game.objects.create(group_name=group_name, player1=player1, player2=player2, status="accepted")
        return game

    @database_sync_to_async
    def get_game(self, game_id):
        # Get the game instance with the given id
        game = Game.objects.get(id=game_id)
        return game

    @database_sync_to_async
    def save_game(self, game):
        # Save the game instance to the database
        game.save()

    @database_sync_to_async
    def record_game(self, game_id, player1_score, player2_score, winner):
        game = Game.objects.get(id=game_id)
        game.status = "ended"
        game.player1_score = player1_score
        game.player2_score = player2_score
        game.winner = winner
        game.save()

    @database_sync_to_async
    def is_user_exist(self, opponent):
        return UserProfile.objects.filter(username=opponent).exists()
    
    @database_sync_to_async
    def is_user_online(self, opponent):
        return UserProfile.objects.filter(username=opponent, status="online").exists()
    
    @database_sync_to_async
    def get_online_users_list(self):
        return [user.username for user in UserProfile.objects.filter(online=True)]
    
    @database_sync_to_async
    def get_user(self, username):
        return UserProfile.objects.get(username=username)
    '''
    @database_sync_to_async
    def create_tournament(self, name):
        # Create a new tournament instance with the given name and an empty standings
        # start_date in models.py is auto_now_add=True maybe we shouldn't pass it here
        tournament = Tournament.objects.create(id=uuid4(), name=name, status="open", start_date=datetime.now(), standings={})
        return tournament
    
    @database_sync_to_async
    def get_tournament(self, tournament_id):
        # Get the tournament instance with the given id
        tournament = Tournament.objects.get(id=tournament_id)
        return tournament
    
    @database_sync_to_async
    def save_tournament(self, tournament):
        # Save the tournament instance to the database
        tournament.save()

    @database_sync_to_async
    def create_matches(self, tournament):
        # Create the next round of matches for the tournament
        # This is a simplified logic that assumes the number of players is a power of two
        # and that the players are ordered by their standings
        players = list(tournament.participants.all())
        matches = []
        for i in range(0, len(players), 2):
            # Create a new match instance with the pair of players and the tournament
            match = Match.objects.create(player1=players[i], player2=players[i+1], tournament=tournament)
            matches.append(match)
        return matches

    @database_sync_to_async
    def get_match(self, match_id):
        # Get the match instance with the given id
        match = Match.objects.get(id=match_id)
        return match

    @database_sync_to_async
    def save_match(self, match):
        # Save the match instance to the database
        match.save()
'''
    # Handler methods for different types of messages
    async def user_online(self, event):
        # Handle a message that a user is online
        username = event["username"]
        users = event["users"]
        # Send a message to the client with the username
        await self.send(text_data=json.dumps({
            "type": "user.online",
            "username": username,
            "users": users,
        }))

    async def user_offline(self, event):
        # Handle a message that a user is offline
        username = event["username"]
        #users = event["users"]
        # Send a message to the client with the username
        await self.send(text_data=json.dumps({
            "type": "user.offline",
            "username": username,
            #"users": users,
        }))

    async def game_invite(self, event):
        # Handle a message that a game is invited
        group_name = event["group_name"]
        inviter = event["inviter"]
        invited = event["invited"]
        # Send a message to the client with the game id and the players' usernames
        await self.send(text_data=json.dumps({
            "type": "game.invite",
            "group_name": group_name,
            "inviter": inviter,
            "invited": invited,
        }))

    async def game_accept(self, event):
        # Handle a message that a game is accepted
        game_id = event["game_id"]
        accepted = event["accepted"]
        accepter = event["accepter"]
        # Send a message to the client with the game id and the players' usernames
        await self.send(text_data=json.dumps({
            "type": "game.accept",
            "game_id": game_id,
            "accepted": accepted,
            "accepter": accepter,
        }))
    
    async def game_decline(self, event):
        # Handle a message that a game is declined
        decliner = event["decliner"]
        declined = event["declined"]
        # Send a message to the client with the game id
        await self.send(text_data=json.dumps({
            "type": "game.decline",
            "declined": declined,
            "decliner": decliner,
        }))


    async def game_start(self, event):
        # Handle a message that a game is started
        game_id = event["game_id"]
        player1 = event["player1"]
        player2 = event["player2"]
        # Send a message to the client with the game id and the players' usernames
        await self.send(text_data=json.dumps({
            "type": "game.start",
            "game_id": game_id,
            "player1": player1,
            "player2": player2,
        }))


    async def game_ball(self, event):
        # Handle a message that a ball move is made in a game
        game_id = event["game_id"]
        x = event["ballX"]
        y = event["ballY"]
        # Send a message to the client with the game id, the move coordinates, and the player's username
        await self.send(text_data=json.dumps({
            "type": "game.ball",
            "game_id": game_id,
            "ballX": x,
            "ballY": y,
        }))

    async def game_paddle(self, event):
        # Handle a message that a paddle move is made in a game
        game_id = event["game_id"]
        y = event["y"]
        player = event["player"]
        # Send a message to the client with the game id, the move coordinates, and the player's username
        await self.send(text_data=json.dumps({
            "type": "game.paddle",
            "game_id": game_id,
            "y": y,
            "player": player,
        }))

    async def game_end(self, event):
        # Handle a message that a game is ended
        game_id = event["game_id"]
        player1_score = event["player1_score"]
        player2_score = event["player2_score"]
        winner = event["winner"]
        # Send a message to the client with the game id and the winner's username
        await self.send(text_data=json.dumps({
            "type": "game.end",
            "game_id": game_id,
            "player1_score": player1_score,
            "player2_score": player2_score,
            "winner": winner,
        }))
'''
    async def tournament_join(self, event):
        # Handle a message that a user joined a tournament
        tournament_id = event["tournament_id"]
        username = event["username"]
        # Send a message to the client with the tournament id and the username
        await self.send(text_data=json.dumps({
            "type": "tournament.join",
            "tournament_id": tournament_id,
            "username": username,
        }))

    async def tournament_start(self, event):
        # Handle a message that a tournament is started
        tournament_id = event["tournament_id"]
        matches = event["matches"]
        # Send a message to the client with the tournament id and the matches details
        await self.send(text_data=json.dumps({
            "type": "tournament.start",
            "tournament_id": tournament_id,
            "matches": matches,
        }))

    async def tournament_finish(self, event):
        # Handle a message that a match is finished in a tournament
        match_id = event["match_id"]
        winner = event["winner"]
        # Send a message to the client with the match id and the winner's username
        await self.send(text_data=json.dumps({
            "type": "tournament.finish",
            "match_id": match_id,
            "winner": winner,
        }))

    async def tournament_next(self, event):
        # Handle a message that the next round of matches is started in a tournament
        tournament_id = event["tournament_id"]
        matches = event["matches"]
        # Send a message to the client with the tournament id and the matches details
        await self.send(text_data=json.dumps({
            "type": "tournament.next",
            "tournament_id": tournament_id,
            "matches": matches,
        }))

    async def tournament_end(self, event):
        # Handle a message that a tournament is ended
        tournament_id = event["tournament_id"]
        winner = event["winner"]
        # Send a message to the client with the tournament id and the winner's username
        await self.send(text_data=json.dumps({
            "type": "tournament.end",
            "tournament_id": tournament_id,
            "winner": winner,
        }))
'''