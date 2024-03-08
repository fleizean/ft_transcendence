from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from .utils import add_to_cache, remove_from_cache
from .models import UserProfile
import json

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            return

        """         # get UserProfile object
        user_profile = await UserProfile.objects.aget(id=self.user.id)
        user_profile.is_online = True
        await user_profile.asave()
        # Add user ID to online_users list
        add_to_cache('online_users', set(), self.user.id) """
        cache.set(f'online_{self.user.username}', True)
        # Maybe add playing to the cache
        await self.accept()

        await self.send(text_data=json.dumps({
            'status': 'online',
        }))


    async def disconnect(self, close_code):
        if self.user.is_anonymous:
            return

        cache.set(f'online_{self.user.username}', False)
        # Maybe add playing to the cache
        """         user_profile = await UserProfile.objects.aget(id=self.user.id)
        user_profile.is_online = False
        await user_profile.asave()
        # Remove user ID from online_users list
        remove_from_cache('online_users', set(), self.user.id) """
        await self.close()

"""
def is_user_online(user):
    return cache.get(f'online_{user.id}') is not None"""

"""
def get_online_users():
    online_user_ids = cache.get('online_users', set())
    return UserProfile.objects.filter(id__in=online_user_ids)"""



"""     # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        await self.channel_layer.group_send(
            'online_status',
            {
                'type': 'online_status_message',
                'message': message
            }
        )

    # Receive message from group
    async def online_status_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        })) """