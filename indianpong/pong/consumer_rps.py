import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game, UserProfile


class RPSConsumer(AsyncWebsocketConsumer):
    players_queue = []

    async def connect(self):
        self.room_name = 'rps_game'
        self.room_group_name = 'rps_game_group'
        await self.accept()

    async def disconnect(self, close_code):
        self.remove_from_queue()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'join_queue':
            await self.join_queue()
        

    async def join_queue(self):
        self.user = self.scope["user"]
        user_elo_point = self.user.elo_point
        print(self.user.username + ": " + str(user_elo_point) + " elo point")
        self.players_queue.append((self.channel_name, user_elo_point))  # Append a tuple
        # Send a message to the user that they have successfully joined the matchmaking queue
        await self.send(text_data=json.dumps({
            'message': 'Successfully joined matchmaking queue.'
        }))
        # Start the process of checking the queue for a match
        await self.check_for_match()

    async def check_for_match(self):
        if len(self.players_queue) >= 2:
            # If there are at least two people in the queue, match the first two people
            player1, player2 = self.players_queue[:2]
            # Check if the elo_point difference is not greater than 100
            if abs(player1[1] - player2[1]) <= 100:
                # If the elo_point difference is not greater than 100, match the players
                # Remove the matched players from the queue
                self.players_queue = self.players_queue[2:]
                # Send a message to the players that they have been matched
                await self.channel_layer.send(player1[0], {
                    'type': 'player.matched',
                    'opponent_channel_name': player2[0]
                })
                await self.channel_layer.send(player2[0], {
                    'type': 'player.matched',
                    'opponent_channel_name': player1[0]
                })
            else:
                # If the elo_point difference is greater than 100, don't match the players
                pass

    def remove_from_queue(self):
        # Kuyruktan ayrılan kullanıcıyı kaldırın
        if self.channel_name in self.players_queue:
            self.players_queue.remove(self.channel_name)

    async def game_match(self, event):
        opponent_channel = event['opponent_channel']

        await self.send(text_data=json.dumps({
            "matched": "true",
            'message': 'You are matched with an opponent!'
        }))

    async def player_matched(self, event):
        # Extract the opponent's channel name from the event
        opponent_channel_name = event['opponent_channel_name']
        # Send a message to the user to let them know they've been matched
        await self.send(text_data=json.dumps({
            'message': f'You have been matched with {opponent_channel_name}.'
        }))

""" 
class RPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'rps_game'
        self.room_group_name = 'rps_game_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Oyuncuyu eşleştirme talebi
        room = await sync_to_async(rpsRoom.get_or_create_waiting_room)()
        room.add_player(self.channel_name)

        # Eğer odada iki oyuncu varsa, oyunu başlat
        if room.is_full():
            opponent_channel_name = room.get_opponent_channel_name(self.channel_name)
            await self.channel_layer.group_send(
                opponent_channel_name,
                {
                    'type': 'game_start',
                    'message': 'Your opponent is ready. Game starting...'
                }
            )
            await self.channel_layer.group_send(
                self.channel_name,
                {
                    'type': 'game_start',
                    'message': 'Opponent found. Game starting...'
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def game_start(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
 """