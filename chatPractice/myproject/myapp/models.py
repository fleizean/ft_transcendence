import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Room(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)

class ChatUser(models.Model):
    user = models.ForeignKey(User, related_name = "chat_user", verbose_name = "Kullanıcı", on_delete = models.CASCADE)
    room = models.ForeignKey(Room, related_name = "chat_users", verbose_name = "Oda", on_delete = models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(User, related_name = "messages", verbose_name = "Kullanıcı", on_delete = models.CASCADE)
    room = models.ForeignKey(Room, related_name = "messages", verbose_name = "Oda", on_delete = models.CASCADE)
    content = models.TextField(verbose_name = "Mesaj içeriği")
    created_date = models.DateField(auto_now_add = True)


