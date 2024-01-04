import json
from uuid import uuid4
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, Tournament, MatchRecord, UserProfile #Match, Score
from datetime import datetime

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope
        self.user = self.scope["user"]
        # Check if the user is authenticated
        if self.user.is_anonymous:
            # Reject the connection
            await self.close()
        # Set the user's channel name
        self.user.channel_name = self.channel_name
        self.user.online = True
        await self.user.asave()
        # Accept the connection
        await self.accept()
        # Add the user to the 'online' group
        await self.channel_layer.group_add("online", self.channel_name)
        # Send a message to the group with the user's username
        online_users = await self.get_online_users_list()
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
        self.user.channel_name = None
        self.user.online = False
        await self.user.asave()
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("online", self.channel_name)
        # Send a message to the group with the user's username
        online_users = await self.get_online_users_list()
        await self.channel_layer.group_send(
            "online",
            {
                "type": "user.offline",
                "username": self.user.username,
                "users": online_users,
            }
        )

    async def receive(self, text_data):
        # Receive a message from the client
        data = json.loads(text_data)
        action = data["action"]
        if action == "invite":
            # Invite another user to play a game
            opponent = data["opponent"]
            # Check if the opponent exists
            if not await self.is_user_exist(opponent):
                # Send a message to the client with the error
                await self.send(text_data=json.dumps({
                    "error": "User does not exist",
                }))
                return
            # Get the opponent instance from the database
            #invited = await self.get_user(opponent)
            invited = await UserProfile.objects.aget(username=opponent)

            # Create a new game instance and save it to the database
            game = await self.create_game(self.user, invited)
            # Add both users to the game group
            await self.channel_layer.group_add(game.group_name, self.user.channel_name)
            await self.channel_layer.group_add(game.group_name, invited.channel_name)
            # Send a message to the game group with the game id and the players' usernames
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.invite",
                    "game_id": game.id,
                    "player1": self.user.username,
                    "player2": invited.username,
                }
            )
        elif action == "accept":
            # Accept an invitation to play a game
            game_id = data["game_id"]
            player1_username = data["player1"]
            player2_username = data["player2"]
            # Get the game instance from the database
            game = await self.get_game(game_id)
            # Update the game status to 'started' and save it to the database
            game.status = "started"
            await self.save_game(game)
            # Send a message to the game group with the game id and the players' usernames
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.start",
                    "game_id": game.id,
                    "player1": player1_username,
                    "player2": player2_username,
                }
            )
        elif action == "decline":
            # Decline an invitation to play a game
            game_id = data["game_id"]
            opponent = data["opponent"]
            # Get the game instance from the database
            game = await self.get_game(game_id)
            # Discard opponent from the game group
            await self.channel_layer.group_discard(game.group_name, opponent.channel_name)
            # Send a message to the game group with the game id
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.decline",
                    "game_id": game.id,
                }
            )
            # Delete the game instance from the database
            await game.delete()
            #await self.close() ?

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
            winner = player1_score > player2_score and game.player1.username or game.player2.username
            # Record the game status to 'ended' and save it to the database
            # Record the game winner, scores and save it to the database
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
    def create_game(self, player1, player2):
        # Create a new game instance with the given players and an empty state
        game = Game.objects.create(group_name=str(uuid4()), player1=player1, player2=player2, status="invited")#, state=[[None]*10 for _ in range(10)])
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
    def get_online_users_list(self):
        return [user.username for user in UserProfile.objects.filter(online=True)]
    
    """ @database_sync_to_async
    def get_user(self, opponent):
        return UserProfile.objects.get(username=opponent) """
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
        users = event["users"]
        # Send a message to the client with the username
        await self.send(text_data=json.dumps({
            "type": "user.offline",
            "username": username,
            "users": users,
        }))

    async def game_invite(self, event):
        # Handle a message that a game is invited
        game_id = event["game_id"]
        player1 = event["player1"]
        player2 = event["player2"]
        # Send a message to the client with the game id and the players' usernames
        await self.send(text_data=json.dumps({
            "type": "game.invite",
            "game_id": game_id,
            "player1": player1,
            "player2": player2,
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

    async def game_decline(self, event):
        # Handle a message that a game is declined
        game_id = event["game_id"]
        # Send a message to the client with the game id
        await self.send(text_data=json.dumps({
            "type": "game.decline",
            "game_id": game_id,
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