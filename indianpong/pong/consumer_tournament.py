from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Tournament, UserProfile
import json

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'tournament_{self.room_name}'
        self.username = self.scope['user'].username

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'create':
            await self.create_tournament(text_data_json)
        elif message_type == 'destroy':
            await self.destroy_tournament(text_data_json)
        elif message_type == 'join':
            await self.join_tournament(text_data_json)
        elif message_type == 'leave':
            await self.leave_tournament(text_data_json)
        elif message_type == 'start':
            await self.start_tournament(text_data_json)

    # Send message to room group
    async def send_room_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message
            }
        )

    # Receive message from room group
    async def room_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def create_tournament(self, message):
        name = message['name']
        creator = message['creator']
        tournament = Tournament.objects.acreate(name=name, creator=creator)
        tournament.participants.aadd(UserProfile.objects.get(username=creator))

        #? Send a message to himself

    async def destroy_tournament(self, message):
        tournament_id = message['tournament_id']
        tournament = Tournament.objects.aget(id=tournament_id)
        if tournament.creator == UserProfile.objects.aget(username=self.username):
            tournament.adelete()
            #? Send a message to himself



    async def join_tournament(self, message):
        tournament_id = message['tournament_id']
        tournament = Tournament.objects.aget(id=tournament_id)
        tournament.participants.aadd(UserProfile.objects.get(username=self.username))
        #? Send a message to the room group
        await self.send_room_message({
            'type': 'joined',
            'username': self.username
        })



    async def leave_tournament(self, message):
        tournament_id = message['tournament_id']
        tournament = Tournament.objects.aget(id=tournament_id)
        tournament.participants.aremove(UserProfile.objects.aget(username=self.username))
        #? Send a message to the room group
        await self.send_room_message({
            'type': 'left',
            'username': self.username
        })


    @database_sync_to_async
    def start_tournament(self, message):
        tournament_id = message['tournament_id']
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.create_first_round_matches()
        # Send first_round_matches to the room group
        self.send_room_message({
            'type': 'first_round_matches',
            'matches': tournament.first_round_matches
        })

    #? This part ll be in game consumer and it ll increase played_games_count
    #? and if played_games_count 2, it ll use create_final_round_matches on tournamen object
    #? and if played_games_count 3, it ll update the tournament object status to ENDED, set winner and send a message to the room group
    @database_sync_to_async
    def end_game(self, message):
        tournamet_id = message['tournament_id']
        game_id = message['game_id']
