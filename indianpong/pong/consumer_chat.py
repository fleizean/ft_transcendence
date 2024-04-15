import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        from .models import UserProfile, Message, Game
        data = json.loads(text_data)
        action = data["action"]
        if action == "chat":
            message = data["message"]
            user = await UserProfile.objects.aget(username=self.user.username)
            m = await Message.objects.acreate(content=message, user=user, room_id=self.room_name) #room_id is the room name
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
            # Send invite message to room group which have accept button and decline button in it
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "invite.game",
                    "inviter": self.user.username,
                }
            )

        elif action == "accept.game":
            # if accept it create game object and send link in form: /remote-game/invite/game_id to both
            # send message to room group that user accepted the game make it in client side
            accepted = data["accepted"]
            accepted = await UserProfile.objects.aget(username=accepted)
            accepter = await UserProfile.objects.aget(username=self.user.username)           
            group_name = f"{accepted}-{accepter}"
            # create game object
            game = await Game.objects.acreate(group_name=group_name, player1=accepted, player2=accepter)
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "accept.game", 
                    "game_id": game.id,
                    "user": accepted.username,
                }
            )

        elif action == "decline.game":
            # if decline it send message to room group that user declined the game
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "decline.game",
                    "decliner": self.user.username,
                }
            )

        elif action == "block":
            blocked = data["blocked"]
            # add user to block list
            me = await UserProfile.objects.aget(username=self.user.username)
            blocked = await UserProfile.objects.aget(username=blocked)
            await me.blocked_users.aadd(blocked)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "blocked",
                    "blocker": self.user.username,
                    "blocked": blocked.username,
                }
            )

        elif action == "unblock":
            # remove user from block list
            blocked = data["unblocked"]
            # add user to block list
            me = await UserProfile.objects.aget(username=self.user.username)
            blocked = await UserProfile.objects.aget(username=blocked)
            await me.blocked_users.aremove(blocked)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "unblocked",
                    "unblocker": self.user.username,
                    "unblocked": blocked.username,
                }
            )

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

    async def invite_game(self, event):
        inviter = event["inviter"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "invite.game",
            "inviter": inviter,
        }))

    async def accept_game(self, event):
        game_id = event["game_id"]
        user = event["user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "accept.game",
            "game_id": game_id,
            "user": user,
        }))

    async def decline_game(self, event):
        decliner = event["decliner"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "decline.game",
            "decliner": decliner,
        }))
    
    async def blocked(self, event):
        # Handle the "blocked" message
        blocker = event["blocker"]
        blocked = event["blocked"]

        await self.send(text_data=json.dumps({
            "type": "blocked",
            "blocker": blocker,
            "blocked": blocked,
        }))

    async def unblocked(self, event):
        # Handle the "unblocked" message
        unblocker = event["unblocker"]
        unblocked = event["unblocked"]

        await self.send(text_data=json.dumps({
            "type": "unblocked",
            "unblocker": unblocker,
            "unblocked": unblocked,
        }))
