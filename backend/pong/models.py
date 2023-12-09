from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(AbstractUser):
    display_name = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

class MatchHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches')
    opponent = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='opponent_matches')
    date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10)  # 'win' or 'lose'

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participants = models.ManyToManyField(UserProfile, related_name='tournaments')

class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    player1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tournament_matches_as_player1')
    player2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tournament_matches_as_player2')
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='tournament_wins')

class OAuthToken(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=16)  # Store the secret key securely
    is_enabled = models.BooleanField(default=False)

class JWTToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
