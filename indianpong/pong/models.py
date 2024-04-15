from email.mime.image import MIMEImage
import os
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils.html import mark_safe
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .utils import create_random_svg, get_upload_to
from indianpong.settings import EMAIL_HOST_USER, STATICFILES_DIRS
from django.utils import timezone
from django.conf import settings
import uuid
from datetime import timedelta
from .game import MAX_SCORE


class Social(models.Model):
    intra42 = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)

class StoreItem(models.Model):
    category_name = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    name_hi = models.CharField(max_length=100, blank=True, null=True)
    name_pt = models.CharField(max_length=100, blank=True, null=True)
    name_tr = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.TextField()
    description = models.TextField()
    description_hi = models.TextField(blank=True, null=True)
    description_pt = models.TextField(blank=True, null=True)
    description_tr = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    keypress = models.CharField(max_length=100, blank=True, null=True)
    show_status = models.BooleanField(default=False) # store'da görünebilir mi?

class UserProfile(AbstractUser):
    displayname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=254)
    avatar = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocked_by')
    social = models.OneToOneField('Social', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_42student = models.BooleanField(default=False)
    is_indianai = models.BooleanField(default=False)
    prefered_lang = models.CharField(max_length=100, blank=True, null=True)
    store_items = models.ManyToManyField(StoreItem, through='UserItem', blank=True)
    game_stats_pong = models.OneToOneField('UserGameStat', on_delete=models.SET_NULL, null=True, blank=True)
    game_stats_rps = models.OneToOneField('UserGameStatRPS', on_delete=models.SET_NULL, null=True, blank=True)
    indian_wallet = models.IntegerField(blank=True, null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    elo_point = models.IntegerField(blank=True, null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(99999)])
    username_change_date = models.DateTimeField(blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        if not self.avatar and self.username != os.environ.get("INDIANAI_USERNAME", default="IndianAI") and self.username != os.environ.get("SUPER_USER", default="Bitlis"):
            svg_content = create_random_svg(self.username)
            self.avatar.save(f"{self.username}.svg", svg_content, save=False)
        if not self.game_stats_pong:
            self.game_stats_pong = UserGameStat.objects.create()
        if not self.game_stats_rps:
            self.game_stats_rps = UserGameStatRPS.objects.create()
        super().save(*args, **kwargs)
    
    @property
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.avatar.url))

    def get_rank_image(self):
        ranks = {
            (1, 150): "iron.webp",
            (150, 200): "bronze.webp",
            (200, 250): "silver.webp",
            (250, 310): "gold.webp",
            (310, 360): "platinum.webp",
            (360, 420): "emerald.webp",
            (420, 500): "diamond.webp",
            (500, 550): "master.webp",
            (550, 600): "grandmaster.webp",
            (600, float('inf')): "challenger.webp"
        }
        for rank_range, rank_image in ranks.items():
            if rank_range[0] <= self.elo_point <= rank_range[1]:
                return rank_image
        return "unranked.webp"

    def get_rank_name(self):
        ranks = {
            (1, 150): "Warritt",
            (150, 200): "Kagen",
            (200, 250): "Larvik",
            (250, 310): "Deglan",
            (310, 360): "Letho",
            (360, 420): "Eskel",
            (420, 500): "Lambert",
            (500, 550): "Vesemir",
            (550, 600): "Geralt of Rivia",
            (600, float('inf')): "Cirilla Fiona"
        }
        for rank_range, rank_name in ranks.items():
            if rank_range[0] <= self.elo_point <= rank_range[1]:
                return rank_name
        return "Reinald"


class UserItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    is_bought = models.BooleanField(default=False) # satın alındı mı?
    is_equipped = models.BooleanField(default=False) # kullanıma alındı mı veya inventorye eklendi mi?
    whatis = models.CharField(max_length=100, blank=True, null=True) # ai name or colors

class UserGameStat(models.Model): #? Pong and RPS models are same
    total_games_pong = models.IntegerField(default=0)
    total_win_pong = models.IntegerField(default=0)
    total_lose_pong = models.IntegerField(default=0)
    total_win_streak_pong = models.IntegerField(default=0)
    total_lose_streak_pong = models.IntegerField(default=0)
    total_win_rate_pong = models.FloatField(default=0.0)
    total_avg_game_duration_pong = models.DurationField(default=timedelta(0), null=True, blank=True)
    total_avg_points_won_pong = models.FloatField(default=0.0)
    total_avg_points_lost_pong = models.FloatField(default=0.0)

    def formatted_game_duration(self):
        if self.total_avg_game_duration_pong is None:
            return None

        total_seconds = int(self.total_avg_game_duration_pong.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the duration as "1h 3m 2s", "3m 2s", "2s", etc.
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def formatted_win_rate(self):
        # Win rate'i yüzde cinsinden hesapla ve float olarak döndür
        win_rate_percentage = self.total_win_rate_pong * 100

        # Win rate'i string olarak formatla
        return f"%{win_rate_percentage:.1f}"

    def formatted_avg_points_lost(self):
        return "{:.2f}".format(self.total_avg_points_lost_pong)

    def formatted_avg_points_won(self):
        return "{:.2f}".format(self.total_avg_points_won_pong)        


class UserGameStatRPS(models.Model):
    total_games_rps = models.IntegerField(default=0)
    total_win_rps = models.IntegerField(default=0)
    total_lose_rps = models.IntegerField(default=0)
    total_win_streak_rps = models.IntegerField(default=0)
    total_lose_streak_rps = models.IntegerField(default=0)
    total_win_rate_rps = models.FloatField(default=0.0)
    total_avg_game_duration_rps = models.DurationField(default=timedelta(0), null=True, blank=True)
    total_avg_points_won_rps = models.FloatField(default=0.0)
    total_avg_points_lost_rps = models.FloatField(default=0.0)

    def formatted_game_duration(self):
        if self.total_avg_game_duration_rps is None:
            return None

        total_seconds = int(self.total_avg_game_duration_rps.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the duration as "1h 3m 2s", "3m 2s", "2s", etc.
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def formatted_win_rate(self):
        # Win rate'i yüzde cinsinden hesapla ve float olarak döndür
        win_rate_percentage = self.total_win_rate_rps * 100

        # Win rate'i string olarak formatla
        return f"%{win_rate_percentage:.1f}"

    def formatted_avg_points_lost(self):
        return "{:.2f}".format(self.total_avg_points_lost_rps)

    def formatted_avg_points_won(self):
        return "{:.2f}".format(self.total_avg_points_won_rps)

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

        """         # List of images
        images = ['github.png', '268a.jpg', 'back.png', 'head.png']

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
            email.attach(img) """

        # Send the email
        email.send(fail_silently=True)
        #send_mail(mail_subject, message, EMAIL_HOST_USER, [user.email], fail_silently=True, html_message=message)



class Game(models.Model):
    GAME_KIND_CHOICES = (
        ("pong", "Pong"),
        ("rps", "Rock Paper Scissors")
    )

    game_kind = models.CharField(max_length=10, choices=GAME_KIND_CHOICES, default="pong") #? Maybe unnecessary
    tournament_id = models.IntegerField(MinValueValidator(1), null=True, blank=True)
    group_name = models.CharField(max_length=100)
    player1 = models.ForeignKey(UserProfile, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(UserProfile, related_name='games_as_player2', on_delete=models.CASCADE)
    winner_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    loser_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    game_duration = models.DurationField(null=True, blank=True)
    winner = models.ForeignKey(UserProfile, related_name='games_won', on_delete=models.CASCADE, null=True, blank=True)
    loser = models.ForeignKey(UserProfile, related_name='games_lost', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username}"
    
    def forfeit(self, forfeiting_user):
        if self.player1 == forfeiting_user:
            self.winner = self.player2
            self.loser = self.player1
            self.loser_score = 0
            self.winner_score = MAX_SCORE
        else:
            self.winner = self.player1
            self.loser = self.player2
            self.winner_score = MAX_SCORE
            self.loser_score = 0
        self.save()
    
    def formatted_game_duration(self):
        if self.game_duration is None:
            return None

        total_seconds = int(self.game_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the duration as "1h 3m 2s", "3m 2s", "2s", etc.
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

class Tournament(models.Model):
    STATUS_CHOICES = (
        ("open", "Opened"),
        ("started", "Started"),
        ("ended", "Ended")
    )

    GAME_MODE_CHOICES = (
        ("vanilla", "Vanilla"),
        ("abilities", "Abilities")
    )

    name = models.CharField(max_length=100)
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES, default="vanilla")
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='creator_tournament')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    start_date = models.DateTimeField(auto_now_add=True)
    #end_date = models.DateTimeField()
    participants = models.ManyToManyField(UserProfile, related_name='tournaments')
    first_round_matches = models.ManyToManyField(Game, related_name='first_round_matches', blank=True)
    final_round_matches = models.ManyToManyField(Game, related_name='final_round_matches', blank=True)
    played_games_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tournament_wins', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def create_first_round_matches(self):
        
        participants = list(self.participants.all())
        random.shuffle(participants)

        for i in range(0, len(participants), 2):
            game = Game.objects.create(
                tournament_id=self.id,
                group_name=f"{participants[i].username}-{participants[i+1].username}",
                player1=participants[i],
                player2=participants[i+1]
            )
            self.first_round_matches.add(game)
            self.message_for_match(game)
        self.status = "started"
        self.save()
        
    def create_final_round_matches(self):
        # Get the winners of the first round matches
        winners = [match.winner for match in self.first_round_matches.all()]
        final_game = Game.objects.create(
            tournament_id=self.id,
            group_name=f"{winners[0].username}-{winners[1].username}",
            player1=winners[0],
            player2=winners[1]
        )
        self.final_round_matches.add(final_game)
        self.message_for_match(final_game)
    
    def message_for_match(self, game):
        # Create room between players if does not exist
        try:
            room = Room.objects.get(first_user=game.player1, second_user=game.player2)
        except Room.DoesNotExist:
            try:
                room = Room.objects.get(second_user=game.player1, first_user=game.player2)
            except Room.DoesNotExist:
                room = Room.objects.create(first_user=game.player1, second_user=game.player2)
        # Create message for the room with game link
        message = f"{settings.BASE_URL}/remote-game/tournament/{game.id}"
        Message.objects.create(user=game.player1, room=room, content=message)
    

class OAuthToken(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    secret_valid_until = models.IntegerField(null=True, blank=True)



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

"""
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

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=16)  # Store the secret key securely
    is_enabled = models.BooleanField(default=False)

class JWTToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
"""