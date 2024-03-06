import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game, UserProfile


class RPSConsumer(AsyncWebsocketConsumer):
    players_queue = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        self.remove_from_queue()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'join_queue':
            await self.join_queue()
        

    async def join_queue(self):
        # Bağlanan kullanıcıyı kuyruğa ekleyin
        self.players_queue.append(self.channel_name)
        # Kullanıcıya kuyruğa başarıyla katıldığına dair bir mesaj gönderin
        await self.send(text_data=json.dumps({
            'message': 'Successfully joined matchmaking queue.'
        }))
        # Kuyrukta eşleşme olup olmadığını kontrol etmek için kuyruğu kontrol etme işlemi başlatın
        await self.check_for_match()

    async def check_for_match(self):
        if len(self.players_queue) >= 2:
            # Eğer kuyrukta en az iki kişi varsa, ilk iki kişiyi eşleştirin
            players_to_match = self.players_queue[:2]
            self.players_queue = self.players_queue[2:]

            # Her iki oyuncuya da eşleşme bilgisini gönderin
            for player_channel in players_to_match:
                await self.channel_layer.send(
                    player_channel,
                    {
                        'type': 'game.match',
                        'opponent_channel': players_to_match[1] if player_channel == players_to_match[0] else players_to_match[0]
                    }
                )

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