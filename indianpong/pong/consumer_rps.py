import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game, UserProfile
import asyncio
import random

class RPSConsumer(AsyncWebsocketConsumer):
    players_queue = []


    # Diğer kodlar...

    async def connect(self):
        self.opponent_selection = None  # Burada opponent_selection özniteliğini tanımlıyoruz
        await self.accept()

    async def disconnect(self, close_code):
        self.remove_from_queue()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        if action == 'make_selection':
            selection = text_data_json.get('selection')
            print(selection)
            await self.make_selection(selection)
        if action == 'join_queue':
            await self.join_queue()
    


    async def make_selection(self, selection):
        print('Bekleniyor')
        # Oyuncunun seçimini kaydedin
        self.selection = selection

        # Eğer rakip de seçimini yapmışsa, karşılaştırma işlemini yapın
        if hasattr(self, 'opponent_selection') and self.opponent_selection:
            await self.compare_selections(self.channel_name, self.opponent_channel, self.selection, self.opponent_selection)
        else:
            # Rakibin seçimini bekleyin
            print('Bekleniyor 2')

            # Önce bir sözlük oluşturuz
            if not hasattr(self, 'waiting_selections'):
                self.waiting_selections = {}

            # Rakibin seçimini bekleyen bir oyuncu olarak kendinizi ekleyin
            self.waiting_selections[self.channel_name] = self.selection

            # Rakip seçimini belirli bir süre içinde yapmazsa, kendisi otomatik bir seçim yapacak
            await asyncio.sleep(3)  # 3 saniye bekle
            if self.opponent_selection is None:
                self.opponent_selection = random.choice(["rock", "paper", "scissors"])  # Otomatik seçim yap
                print(f"Rakip oyuncu otomatik olarak {self.opponent_selection} seçti.")

                # Otomatik seçim yapıldığında, karşılaştırma işlemini yapın
                await self.compare_selections(self.channel_name, self.opponent_channel, self.selection, self.opponent_selection)
            else:
                # Rakip seçim yapıldıysa, onu compare_selections'a gönderin
                await self.compare_selections(self.channel_name, self.opponent_channel, self.selection, self.opponent_selection)

    
    async def compare_selections(self, own_channel, opponent_channel, own_selection, opponent_selection):
        # Oyuncuların seçimlerini karşılaştırın ve sonucu belirleyin
        print('Karsilastiriliyor')
        result = None
        if own_selection == opponent_selection:
            result = "Draw"
        elif own_selection == "rock":
            result = "Win" if opponent_selection == "scissors" else "Lose"
        elif own_selection == "paper":
            result = "Win" if opponent_selection == "rock" else "Lose"
        elif own_selection == "scissors":
            result = "Win" if opponent_selection == "paper" else "Lose"

        # Sonucu her iki oyuncuya da gönderin
        await self.channel_layer.group_send(
            own_channel,
            {
                'type': 'game.result',
                'result': result
            }
        )
        await self.channel_layer.group_send(
            opponent_channel,
            {
                'type': 'game.result',
                'result': "Win" if result == "Lose" else "Lose" if result == "Win" else "Draw"
            }
        )


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