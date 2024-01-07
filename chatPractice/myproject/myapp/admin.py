from django.contrib import admin
from .models import Room, ChatUser, Message

# Register your models here.
admin.site.register(Room)

@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ["user", "room"]
    
    class Meta:
        model = ChatUser

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "room", "created_date"]
    
    class Meta:
        model = Message