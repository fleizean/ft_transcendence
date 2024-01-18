from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
import uuid

class UserProfile(AbstractUser):
    displayname = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False)
    #channel_name = models.CharField(max_length=100, blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.username}"
    
    @property
    def thumbnail(self):
        if self.avatar:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.avatar.url))
        else:
            return mark_safe('<img src="/static/assets/profile/default_avatar.jpeg" width="50" height="50" />')
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class BlockedUser(models.Model):
    user = models.ForeignKey(UserProfile, related_name='blocking_users', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(UserProfile, related_name='blocked_by_users', on_delete=models.CASCADE)

class GameInvitation(models.Model):
    inviting_user = models.ForeignKey(UserProfile, related_name='invitations_sent', on_delete=models.CASCADE)
    invited_user = models.ForeignKey(UserProfile, related_name='invitations_received', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inviting_user.username} invited {self.invited_user.username} to play Pong"
    
class GameWarning(models.Model):
    user = models.ForeignKey(UserProfile, related_name='warnings_sent', on_delete=models.CASCADE)
    opponent = models.ForeignKey(UserProfile, related_name='warnings_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} sent a game warning to {self.opponent.username}"

class Game(models.Model):

    group_name = models.CharField(max_length=100)
    player1 = models.ForeignKey(UserProfile, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(UserProfile, related_name='games_as_player2', on_delete=models.CASCADE)
    player1_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    player2_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(UserProfile, related_name='games_won', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username}"

class MatchRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches')
    opponent = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='opponent_matches')
    date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10)  # 'win' or 'lose'

    def __str__(self) -> str:
        return f"{self.user + '-' + self.opponent}"

class Tournament(models.Model):
    STATUS_CHOICES = (
        ("open", "Opened"),
        ("started", "Started"),
        ("ended", "Ended")
    )

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    start_date = models.DateTimeField(auto_now_add=True)
    #end_date = models.DateTimeField()
    participants = models.ManyToManyField(UserProfile, related_name='tournaments')

    def __str__(self) -> str:
        return f"{self.name}"
    
class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    player1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tournament_matches_as_player1')
    player2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tournament_matches_as_player2')
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='tournament_wins')

class OAuthToken(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField(default=None ,null=True, blank=True)

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=16)  # Store the secret key securely
    is_enabled = models.BooleanField(default=False)

class JWTToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()


#------------------------------------------------------------#
    
class Room(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    first_user = models.ForeignKey(UserProfile, related_name = "room_first", on_delete = models.CASCADE, null = True)
    second_user = models.ForeignKey(UserProfile, related_name = "room_second", on_delete = models.CASCADE, null = True)


class Message(models.Model):
    user = models.ForeignKey(UserProfile, related_name = "message_user", on_delete = models.CASCADE)
    room = models.ForeignKey(Room, related_name = "message_room", on_delete = models.CASCADE)
    content = models.TextField(verbose_name = "Text Content")
    created_date = models.DateTimeField(auto_now_add = True)

    def get_short_date(self):
        return str(self.created_date.strftime("%H:%M"))
