from email.mime.image import MIMEImage
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .utils import get_upload_to
from indianpong.settings import EMAIL_HOST_USER, STATICFILES_DIRS
from django.utils import timezone
import uuid



class Social(models.Model):
    stackoverflow = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)

class Store(models.Model):
    product_name = models.CharField(max_length=200, blank=True, null=True)
    product_description = models.CharField(max_length=200, blank=True, null=True)
    product_price = models.IntegerField(blank=True, null=True)
    product_buystatus = models.BooleanField(default=False)
    product_status = models.BooleanField(default=True)

class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=254)
    avatar = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    social = models.OneToOneField('Social', on_delete=models.CASCADE, null=True, blank=True)
    #channel_name = models.CharField(max_length=100, blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_42student = models.BooleanField(default=False)
    pong_wallet = models.IntegerField(blank=True, null=True, default=0)
    store = models.OneToOneField('Store', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.username}"
    
    @property
    def thumbnail(self):
        if self.avatar:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.avatar.url))
        else:
            return mark_safe('<img src="/static/assets/profile/profilephoto.jpeg" width="50" height="50" />')
        

class VerifyToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def send_verification_email(self, request, user):
        token = VerifyToken.objects.get(user=user)
        mail_subject = 'Activate your account.'
        message = render_to_string('activate_account_email.html', {
            'user': user,
            'domain': request.META['HTTP_HOST'],
            'token': token.token,
        })

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,  # this is the simple text version
            from_email=EMAIL_HOST_USER,
            to=[user.email]
        )

        # Add the HTML version. This could be the same as the body if your email is only HTML.
        email.attach_alternative(message, "text/html")

        # List of images
        images = ['1_icons8-github-50.png', '2_68747470733a.jpg', 'background_2.png', 'header3.png']

        for img_name in images:
            img_path = os.path.join(STATICFILES_DIRS[0], "assets", "email", img_name)

            # Open the image file in binary mode
            with open(img_path, 'rb') as f:
                image_data = f.read()

            # Create a MIMEImage
            img = MIMEImage(image_data)

            # Add a 'Content-ID' header. The angle brackets are important.
            img.add_header('Content-ID', f'<{img_name}>')

            # Attach the image to the email
            email.attach(img)

        # Send the email
        email.send(fail_silently=True)
        #send_mail(mail_subject, message, EMAIL_HOST_USER, [user.email], fail_silently=True, html_message=message)

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
    expires_in = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    secret_valid_until = models.IntegerField(null=True, blank=True)

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
