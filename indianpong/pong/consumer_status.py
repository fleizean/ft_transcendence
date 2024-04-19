from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
#from .models import UserProfile
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
        cache.set(f'playing_{self.user.username}', False) #TODO spada çalışmıyabilir
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
