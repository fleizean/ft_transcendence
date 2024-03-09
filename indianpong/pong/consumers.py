import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from pong.utils import AsyncLockedDict
from .models import Game, Tournament, UserProfile, Room, Message#Match, Score, chat
from pong.game import *

USER_CHANNEL_NAME = AsyncLockedDict() # key: username, value: channel_name
USER_STATUS = AsyncLockedDict() # key: username, value: game_id or online
GAMES = AsyncLockedDict() # key: game_id, value: PongGame object



class PongConsumer(AsyncWebsocketConsumer):
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
        # Accept the connection
        await self.accept()
        # Add the user to the 'online' group
        await self.channel_layer.group_add("online", self.channel_name)
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
                        "type": "user.reconnected",
                        "username": self.user.username,
                    }
                )
        else:
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
        # Remove the user from USER_CHANNEL_NAME and USER_STATUS
        await USER_CHANNEL_NAME.delete(self.user.username)
        # Remove the user from the 'online' group
        await self.channel_layer.group_discard("online", self.channel_name)
        # Remove the user from the game group
        if self.room_group_name != None:
            # Leave room group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Close the websocket connection
        await self.close(close_code)

        game_id = await USER_STATUS.get(self.user.username)
        if game_id != 'online' and game_id != None:
            game = await GAMES.get(game_id)
            #Send opponent a message that the user has disconnected
            await self.channel_layer.group_send(
                game.group_name,
                {
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

        ### CHAT ###
        if action == "room":
            room_name = data["room_name"]
            self.room_name = room_name
            self.room_group_name = "chat_%s" % room_name

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        elif action == "message":
            user = data["user"]
            message = data["message"]
            # Create Message Object
            room = await Room.objects.aget(room_name=self.room_name)
            user = await UserProfile.objects.aget(username = user)
            msg = await Message.objects.acreate(content=message, user=user, room=room)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "chat.message", 
                    "message": message,
                    "user": user.username,
                    "created_date": msg.get_short_date(),
                }
            )
        ### GAME ###
        elif action == "invite": #* Validated
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

            await self.accept_handler(group_name, accepted, accepter)

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
            await self.leave_handler(game_id, left, opponent)

        elif action == "ball": #? Needs validation
            # Make a move in a game and get the ball coordinates
            # we send a message to the clients with the ball coordinates
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
                    await self.end_handler(game_id, game)

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
        ### TOURNAMENT

        elif action == "create":
            # Create a new tournament
            name = data["name"]
            #start_date = data["start_date"]
            #end_date = data["end_date"]
            # Create a new tournament instance with the given details and save it to the database
            tournament = await Tournament.objects.acreate(name)
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
            tournament = await Tournament.objects.aget(id = tournament_id)
            # Add the user to the tournament players and save it to the database
            tournament.standings.add(self.user)
            await tournament.asave()
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
            tournament = await Tournament.objects.aget(id = tournament_id)
            # Remove the user from the tournament players and save it to the database
            tournament.standings.remove(self.user)
            await tournament.asave()
            # Send a message to the 'online' group with the tournament id and the user's username
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.leave",
                    "tournament_id": tournament.id,
                    "username": self.user.username,
                }
            )
        elif action == "cancel": # TODO Only the tournament creator can cancel the tournament
            # Cancel a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await Tournament.objects.aget(id = tournament_id)
            # Delete the tournament instance from the database
            await tournament.adelete()
            # Send a message to the 'online' group with the tournament id
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.cancel",
                    "tournament_id": tournament.id,
                }
            )
        elif action == "start": # TODO Only the tournament creator can start the tournament
            # Start a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await Tournament.objects.aget(id = tournament_id)
            # Update the tournament status to 'started' and save it to the database
            tournament.status = "started"
            await tournament.asave()
            # Create the first round of matches and save them to the database
            matches = await self.create_matches(tournament)
            # Send a message to the 'online' group with the tournament id and the matches details
            for match in matches:
                await self.accept_handler(match.group_name, match.player1.username, match.player2.username, tournament_id)
            """             await self.channel_layer.group_send(
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
            ) """
            """         elif action == "finish":  # TODO move logic to end_handler
            # Finish a match in a tournament
            tournament_id = data["tournament_id"]
            match_id = data["match_id"]
            winner = data["winner"]
            # Get the match instance from the database
            match = await GAMES.get(match_id)
            # Update the match status to 'finished' and save it to the database
            match.status = Status.ENDED
            await Game.objects.asave(id = match_id)
            # Remove loser from the standings and save it to the database
            tournament = await Tournament.objects.aget(id = tournament_id)
            loser =  match.player1.username == winner and match.player2.username or match.player1.username
            loser = await UserProfile.objects.aget(username = loser)
            tournament.standings.remove(loser)
            # Send a message to the 'online' group with the match id and the winner's username
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.finish",
                    "match_id": match.id,
                    "winner": winner,
                }
            ) """
        elif action == "next": # TODO Somehow check if all players finished their matches
            # Start the next round of matches in a tournament
            tournament_id = data["tournament_id"]
            # Get the tournament instance from the database
            tournament = await Tournament.objects.aget(id = tournament_id)
            # Check if the tournament is over
            if await tournament.standings.acount() == 1:
                # Update the tournament status to 'ended' and save it to the database
                tournament.status = "ended"
                await tournament.asave()
                # Send a message to the 'online' group with the tournament id and the winner's username
                await self.channel_layer.group_send(
                    "online",
                    {
                        "type": "tournament.end",
                        "tournament_id": tournament.id,
                        "winner": tournament.standings.username, #? Is this correct?
                    }
                )
            else:
                # Create the next round of matches and save them to the database
                matches = await self.create_matches(tournament)
                # Send a message to the 'online' group with the tournament id and the matches details
                for match in matches:
                    await self.accept_handler(match.group_name, match.player1.username, match.player2.username, tournament_id)
                """                 await self.channel_layer.group_send(
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
                ) """

    # Handler methods for indivual or tournament games
    async def accept_handler(self, group_name, accepted, accepter, tournament_id=None):
        # Create a new game instance and save it to the database
        game = await self.create_game(group_name, accepted, accepter, tournament_id)
        # Create a new game instance and save it to the cache
        await GAMES.set(game.id, PongGame(accepted, accepter, tournament_id))
        if tournament_id != None:
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.match",
                    "tournament_id": tournament_id,
                    "match_id": game.id,
                    "player1": game.player1.username,
                    "player2": game.player2.username,

                }
            )
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

    async def leave_handler(self, game_id, left, opponent):
        # Get scores
        game = await GAMES.get(game_id) 
        left_score = game.getScore(left) # blocking?
        opponent_score = MAX_SCORE # set max score automaticaly
        # Record the game
        await self.record_game(game_id, left_score, opponent_score, opponent)
        # Send a message to the game group with the game id and the opponent's username
        if game.tournament_id != None:
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.match.leave",
                    "tournament_id": game.tournament_id,
                    "match_id": game_id,
                    "left_score": left_score,
                    "opponent_score": opponent_score,
                    "winner": opponent,
                }
            )
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

    async def end_handler(self, game_id, game):
        # Get scores
        player1_score = game.player1.score
        player2_score = game.player2.score
        winner = player1_score > player2_score and game.player1.username or game.player2.username
        # Set the game winner, scores and save it to the database
        await self.record_game(game_id, player1_score, player2_score, winner)
        # Send a message to the game group with the game id and the winner's username
        if game.tournament_id != None:
            # Remove loser from the standings and save it to the database #TODO
            await self.channel_layer.group_send(
                "online",
                {
                    "type": "tournament.match.end",
                    "tournament_id": game.tournament_id,
                    "match_id": game_id,
                    "player1_score": player1_score,
                    "player2_score": player2_score,
                    "winner": winner,
                }
            )
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
        # delete game from cache
        await GAMES.delete(game_id)

    # Helper methods to interact with the database
    async def create_game(self, group_name, player1, player2, tournament_id=None):
        # Create a new game instance with the given players and an group_name
        accepted = await UserProfile.objects.aget(username=player1)
        accepter = await UserProfile.objects.aget(username=player2)
        tournament = await Tournament.objects.aget(id=tournament_id) if tournament_id != None else None            
        game = await Game.objects.acreate(group_name=group_name, player1=accepted, player2=accepter, tournament=tournament)
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
    
    
    @database_sync_to_async
    def create_matches(self, tournament):
        # Create the next round of matches for the tournament
        # This is a simplified logic that assumes the number of players is a power of two
        players = list(tournament.standings.all())
        random.shuffle(players)
        matches = []
        for i in range(0, len(players), 2):
            # Create a new match instance with the pair of players and the tournament
            match = Game.objects.create(player1=players[i], player2=players[i+1], tournament=tournament)
            matches.append(match)
        return matches


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
        }))

    async def user_reconnected(self, event):
        # Handle a message that a user is reconnected
        username = event["username"]
        # Send a message to the client with the username
        await self.send(text_data=json.dumps({
            "type": "user.reconnected",
            "username": username,
        }))

    async def user_disconnected(self, event):
        # Handle a message that a user is disconnected
        username = event["username"]
        # Send a message to the client with the username
        await self.send(text_data=json.dumps({
            "type": "user.disconnected",
            "username": username,
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_date = event["created_date"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "chat.message",
            "message": message,
            "user": user,
            "created_date": created_date,
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
