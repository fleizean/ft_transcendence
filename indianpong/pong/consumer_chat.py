import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        from .models import UserProfile, Message
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        if action == "chat":
            message = text_data_json["message"]
            user = await UserProfile.objects.aget(username = text_data_json["user"])
            m = await Message.objects.acreate(content=message, user=user, room_id=self.room_name) #? Room object isn't created yet
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "chat.message", 
                    "message": message,
                    "user": user.username,
                    "created_date": m.get_short_date(), #? blocking?
                }
            )

        elif action == "invite.game":
            pass
        elif action == "accept.game":
            pass
        elif action == "decline.game":
            pass
        elif action == "block":
            pass
        elif action == "unblock":
            pass

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