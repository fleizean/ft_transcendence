import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RPSGame, Game, UserProfile


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
        self.players_queue.append((self.channel_name, user_elo_point, self.user.email))  # Append a tuple
        # Send a message to the user that they have successfully joined the matchmaking queue
        await self.send(text_data=json.dumps({
            'message': 'Successfully joined matchmaking queue.'
        }))
        # Start the process of checking the queue for a match
        await self.check_for_match()

    async def game_start(self, event):
        player1 = await database_sync_to_async(UserProfile.objects.get)(email=self.user.email)
        player2 = await database_sync_to_async(UserProfile.objects.get)(email=event['opponent_email'])
        print(self.user.username + " game_start")
        print(player1.displayname + " game_start1")
        print(player2.displayname + " game_start2")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        # RPSGame modelinde bir oyun oluştur
        game = await database_sync_to_async(RPSGame.objects.create)(
            # Burada gerekli alanları doldurun, örneğin:
            player1=player1,
            player2=player2
        )
        # Yeni oluşturulan oyunun kimlik numarasını al
        print("game_start")
        game_id = game.room_id
        # Oyunculara oyunun kimlik numarasını gönder
        await self.channel_layer.group_send(
            self.channel_name,
            {
                'type': 'game_id',
                'game_id': str(game_id)
            }
        )
        await self.channel_layer.group_send(
            event['opponent_channel_name'],
            {
                'type': 'game_id',
                'game_id': str(game_id)
            }
        )

    async def game_id(self, event):
        # Oyun kimlik numarasını alır ve oyuncuya gönderir
        game_id = event['game_id']
        await self.send(text_data=json.dumps({
            'game_id': game_id
        }))
    
    async def check_for_match(self):
        if len(self.players_queue) >= 2:
            # If there are at least two people in the queue, match the first two people
            player1, player2 = self.players_queue[:2]
            # Check if the elo_point difference is not greater than 100
            if abs(player1[1] - player2[1]) <= 100:
                # If the elo_point difference is not greater than 100, match the players
                # Remove the matched players from the queue
                self.players_queue = self.players_queue[2:]
                # Call game_start function to start the game
                print(player1[2] + " check_for_match")
                print(player2[2] + " check_for_match")
                await self.game_start({
                    'message': 'Opponent found. Game starting...',
                    'opponent_channel_name': player1[0],
                    'opponent_email': player1[2]  # or player2[0], whichever you prefer
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
"""     async def game_start(self, event):
        try:
            player1 = UserProfile.objects.get(displayname='self.user.username')
        except UserProfile.DoesNotExist:
            print("No UserProfile with username 'player1' exists.")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        # RPSGame modelinde bir oyun oluştur
        game = RPSGame.objects.create(
            # Burada gerekli alanları doldurun, örneğin:
            player1=self.channel_name,
            player2=event['opponent_channel_name']
        )
        print("game_start")
        # Yeni oluşturulan oyunun kimlik numarasını al
        game_id = game.room_id
        # Oyunculara oyunun kimlik numarasını gönder
        await self.channel_layer.group_send(
            self.channel_name,
            {
                'type': 'game_id',
                'game_id': str(game_id)
            }
        )
        await self.channel_layer.group_send(
            event['opponent_channel_name'],
            {
                'type': 'game_id',
                'game_id': str(game_id)
            }
        )
 """

"""     async def check_for_match(self):
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
                pass """
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