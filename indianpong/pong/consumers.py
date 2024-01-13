import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from pong.utils import AsyncLockedDict
from .models import Game, Tournament, MatchRecord, UserProfile, Room, Message #Match, Score, chat
from pong.game import *

USER_CHANNEL_NAME = AsyncLockedDict() # key: username, value: channel_name
USER_STATUS = AsyncLockedDict() # key: username, value: game_id or online
GAMES = AsyncLockedDict() # key: game_id, value: PongGame object

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope
        self.user = self.scope["user"]
        # Check if the user is authenticated
        if self.user.is_anonymous:
            # Reject the connection
            await self.close()
        # Set the user's channel name
        await USER_CHANNEL_NAME.set(self.user.username, self.channel_name)
        #self.user.channel_name = self.channel_name
        #await self.user.asave()
        # Accept the connection
        await self.accept()
        # Add the user to the 'online' group
        await self.channel_layer.group_add("online", self.channel_name)
        # Set the user's status to 'online'
        await USER_STATUS.set(self.user.username, 'online')
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
        #self.user.channel_name = None
        game_id = await USER_STATUS.get(self.user.username)
        if game_id != 'online' and game_id != None:
            # Check if user's username is in any game and that game is not ended
            game = await GAMES.get(game_id)
            if game.status == Status.STARTED: # 2 means game is started
                await self.record_for_disconnected(game_id, game)
            # Delete game cache
            await GAMES.delete(game_id)
            # Remove both users from the game group
            player1_channel_name = await USER_CHANNEL_NAME.get(game.player1.username)
            player2_channel_name = await USER_CHANNEL_NAME.get(game.player2.username)
            await self.channel_layer.group_discard(game.group_name, player1_channel_name)
            await self.channel_layer.group_discard(game.group_name, player2_channel_name)
        # Remove the user's channel name
        await USER_CHANNEL_NAME.delete(self.user.username)
        # make it offline
        await USER_STATUS.delete(self.user.username) 
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("online", self.channel_name)
        # Send a message to the group with the user's username
        await self.channel_layer.group_send(
            "online",
            {
                "type": "user.offline",
                "username": self.user.username,
            }
        )

    async def receive(self, text_data):
        # Receive a message from the client
        data = json.loads(text_data)
        action = data["action"]
        if action == "invite": #* Validated
            # Invite another user to play a game
            invited = data["invited"]
            # Check if the opponent exists #TODO remove these when you implement button invite
            if invited == self.user.username:
                await self.send(text_data=json.dumps({
                    "error": "You can't invite yourself",
                }))
                return
            if not await self.check_is_user_exist(invited):
                return
            #Check if the opponent is online
            if not await self.check_is_user_online(invited):
                return
            # Get the invited channel name
            invited_channel_name = await USER_CHANNEL_NAME.get(invited)
            # Set game group name
            group_name = self.user.username + "-" + invited #str(uuid4())
            # Add both users to the game group
            await self.channel_layer.group_add(group_name, self.channel_name)
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
        elif action == "accept":  #? Needs validation
            # Accept an invitation to play a game
            group_name = data["group_name"]
            accepted = data["accepted"]
            accepter = data["accepter"]
            # Create a new game instance and save it to the database
            game = await self.create_game(group_name, accepted, accepter)
            # Create a new game instance and save it to the cache
            await GAMES.set(game.id, PongGame(accepted, accepter))
            # Send a message to the game group with the game id and the players' usernames
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.accept",
                    "game_id": game.id,
                    "accepter": accepter,
                    "accepted": accepted
                }
            )
        elif action == "decline": #? Needs validation
            # Decline an invitation to play a game
            group_name = data["group_name"]
            declined = data["declined"]
            decliner = data["decliner"]
            declined_channel_name = await USER_CHANNEL_NAME.get(declined)
            # Send a message to the game group with the game id
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "game.decline",
                    "decliner": decliner,
                    "declined": declined,
                }
            )
            # Discard both from the game group
            await self.channel_layer.group_discard(group_name, self.channel_name)
            await self.channel_layer.group_discard(group_name, declined_channel_name)
        elif action == "start.request": #? Needs validation
            # Start a game
            game_id = data["game_id"]
            player1 = data["player1"]
            player2 = data["player2"]
            vote = data["vote"]
            # Get the current game status and update it with the vote count
            game = await GAMES.get(game_id)
            current = game.status.value + int(vote)
            await GAMES.set_field_value(game_id, Status(current), "status")
            # Check both players voted to start the game
            if Status(current) == Status.STARTED: # both players voted to start the game
                # Update the players' status to game_id and save them to cache
                await USER_STATUS.set(player1, game_id)
                await USER_STATUS.set(player2, game_id)
                # Send a message to the game group with the game id
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.start",
                    "game_id": game_id,
                    "player1": player1,
                    "player2": player2,
                    "vote": current,
                }
            )
        elif action == "leave.game": #? Needs validation
            # Leave a game
            game_id = data["game_id"]
            left = data["left"]
            opponent = data["opponent"]
            # Get scores
            game = await GAMES.get(game_id) 
            left_score = game.getScore(left) # blocking?
            opponent_score = MAX_SCORE # set max score automaticaly
            # Record the game
            await self.record_game(game_id, left_score, opponent_score, opponent)
            # Send a message to the game group with the game id and the opponent's username
            await self.channel_layer.group_send(
                game.group_name,
                {
                    "type": "game.leave",
                    "game_id": game_id,
                    "left_score": left_score,
                    "opponent_score": opponent_score,
                    "winner": opponent,
                }
            )
            # Discard both from the game group
            standing_channel_name = await USER_CHANNEL_NAME.get(opponent)
            await self.channel_layer.group_discard(game.group_name, self.channel_name)
            await self.channel_layer.group_discard(game.group_name, standing_channel_name)
            # Update the game status to 'ended' or delete it
            await GAMES.delete(game_id)
        elif action == "ball": #? Needs validation
            # Make a move in a game # TODO this should be in server side not client side?
            # Interval should be 16 ms so every 16 ms
            # we should send a message to the clients with the ball coordinates
            game_id = data["game_id"]
            # Move and Get ball coordinates
            game = await GAMES.get(game_id) #? When games status is ended, game_id is deleted from GAMES cache
            if (game != None): #? So game becomes None. Is this check enough? or moving delete to end solve without this
                if (game.status == Status.STARTED):
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
                elif (game.status == Status.ENDED):
                    # Get scores
                    player1_score = game.player1.score
                    player2_score = game.player2.score
                    winner = player1_score > player2_score and game.player1.username or game.player2.username
                    # Set the game winner, scores and save it to the database
                    await self.record_game(game_id, player1_score, player2_score, winner)
                    # Send a message to the game group with the game id and the winner's username
                    await self.channel_layer.group_send(
                        game.group_name,
                        {
                            "type": "game.end",
                            "game_id": game_id,
                            "player1_score": player1_score, #? maybe redundant
                            "player2_score": player2_score,
                            "winner": winner,
                        }
                    )
                    # Set the game status to 'ended' or delete it
                    await GAMES.delete(game_id)
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
    def get_online_users_list(self):
        return [user.username for user in UserProfile.objects.filter(online=True)]
    
    async def create_game(self, group_name, player1, player2):
        # Create a new game instance with the given players and an group_name
        accepted = await UserProfile.objects.aget(username=player1)
        accepter = await UserProfile.objects.aget(username=player2)
        game = await Game.objects.acreate(group_name=group_name, player1=accepted, player2=accepter)
        return game

    async def record_game(self, game_id, player1_score, player2_score, winner):
        game = await Game.objects.aget(id=game_id)
        await USER_STATUS.set(game.player1.username, 'online') #?
        await USER_STATUS.set(game.player2.username, 'online') #?
        game.player1_score = player1_score
        game.player2_score = player2_score
        game.winner = await UserProfile.objects.aget(username=winner)
        await game.asave()

    async def record_for_disconnected(self, game_id, game):
        if game.player1.username == self.user.username:
            await self.record_game(game_id, game.player1.score, MAX_SCORE, game.player2.username)
        else:
            await self.record_game(game_id, MAX_SCORE, game.player2.score, game.player1.username)

    async def check_is_user_exist(self, username):
        answer = await UserProfile.objects.filter(username=username).aexists()
        if not answer:
            await self.send(text_data=json.dumps({
                "error": "User doesn't exist",
            }))
        return answer
    
    async def check_is_user_online(self, username):
        answer = await USER_STATUS.get(username) == 'online'
        if not answer:
            await self.send(text_data=json.dumps({
                "error": "User is already playing",
            }))
        return answer
    
    
        
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
        # Handle a message that a vote is made to start a game
        game_id = event["game_id"]
        player1 = event["player1"]
        player2 = event["player2"]
        vote = event["vote"]
        # Send a message to the client with the game id and the players' usernames
        await self.send(text_data=json.dumps({
            "type": "game.start",
            "game_id": game_id,
            "player1": player1,
            "player2": player2,
            "vote": vote,
        }))

    async def game_leave(self, event):
        # Handle a message that a game is left
        game_id = event["game_id"]
        left_score = event["left_score"]
        opponent_score = event["opponent_score"]
        winner = event["winner"]
        # Send a message to the client with the game id
        await self.send(text_data=json.dumps({
            "type": "game.leave",
            "game_id": game_id,
            "left_score": left_score,
            "opponent_score": opponent_score,
            "winner": winner,
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

    async def game_ball(self, event):
        # Handle a message that a ball move is made in a game
        game_id = event["game_id"]
        x = event["x"]
        y = event["y"]
        player1_score = event["player1_score"]
        player2_score = event["player2_score"]
        # Send a message to the client with the game id, the move coordinates, and the player's username
        await self.send(text_data=json.dumps({
            "type": "game.ball",
            "game_id": game_id,
            "x": x,
            "y": y,
            "player1_score": player1_score,
            "player2_score": player2_score,
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


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        user = await UserProfile.objects.aget(username = text_data_json["user"])
        m = await Message.objects.acreate(content=message, user=user, room_id=self.room_name) #? Room object isn't created yet
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                "user": user.username,
                "created_date": m.get_short_date(), #? blocking?
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_date = event["created_date"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "created_date": created_date,
        }))