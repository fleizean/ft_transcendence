from django import forms
from django.contrib import admin
from .models import RPSGame, OAuthToken, Social, UserItem, StoreItem, UserProfile, Tournament, Room, Message, Game, UserGameStat
from django.utils.html import format_html
from django.forms import ModelChoiceField


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin class for managing user profiles.

    Attributes:
        list_display (tuple): A tuple of fields to be displayed in the admin list view.
        search_fields (tuple): A tuple of fields to be used for searching in the admin list view.
        fieldsets (tuple): A tuple of fieldsets to be displayed in the admin edit view.
    """

    list_display = ('username', 'email', 'displayname', 'avatar_thumbnail')
    search_fields = ('username', 'email', 'displayname')
    fieldsets = (
    ('User Information', {'fields': ('username', 'password', 'displayname', 'email', 'avatar', 'friends', 'elo_point', 'indian_wallet')}),
    ('Dates', {'fields': ('date_joined', 'last_login')}),
    ('Roles', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified', 'is_42student', 'is_indianai')}),
    ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    def avatar_thumbnail(self, obj):
        return format_html(obj.thumbnail)
    avatar_thumbnail.short_description = 'Avatar'

@admin.register(StoreItem)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'name', 'name_hi', 'name_pt', 'name_tr', 'image_url', 'description', 'description_hi', 'description_pt', 'description_tr', 'price', 'keypress', 'show_status')
    search_fields = ('name', 'description')

    def __str__(self):
        return self.name
    
class UserItemForm(forms.ModelForm):
    class Meta:
        model = UserItem
        fields = ('user', 'item', 'whatis', 'is_bought', 'is_equipped')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].label_from_instance = lambda obj: obj.name

@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    form = UserItemForm
    list_display = ('user', 'get_item_name', 'whatis', 'is_bought', 'is_equipped')
    list_filter = ('is_equipped',)
    search_fields = ('user__username', 'item__name')

    def get_item_name(self, obj):
        return obj.item.name
   
    get_item_name.short_description = 'Item Name'

@admin.register(UserGameStat)
class UserGameStatAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'total_games_pong', 'total_win_pong', 'total_lose_pong', 'total_win_streak_pong', 'total_win_rate_pong', 'total_lose_streak_pong', 'total_avg_game_duration_pong', 'total_avg_points_won_pong', 'total_avg_points_lost_pong')
    search_fields = ('userprofile__username', 'total_win_pong',)

    def get_user(self, obj):
        return obj.userprofile
    get_user.short_description = 'User'

@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'intra42', 'linkedin', 'github', 'twitter')

    def get_user(self, obj):
        return obj.userprofile
    get_user.short_description = 'User'

    search_fields = ('userprofile__username', 'intra42', 'linkedin', 'github', 'twitter')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_kind' ,'group_name', 'player1', 'player2', 'player1_score', 'player2_score', 'created_at', 'game_duration', 'winner', 'loser')
    list_filter = ('player1', 'player2', 'winner', 'loser')
    search_fields = ('player1__username', 'player2__username', 'group_name')

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'winner', 'start_date', 'status')
    search_fields = ('name', 'status')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["first_user", "second_user"]
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "room", "created_date"]


@admin.register(OAuthToken)
class OAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'refresh_token', 'expires_in', 'created_at', 'secret_valid_until')
    search_fields = ('user__username',) 

@admin.register(RPSGame)
class RPSGameAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2')
    list_filter = ('player1', 'player2')
    search_fields = ('player1__username', 'player2__username')

""" @admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled')
    search_fields = ('user__username',)

@admin.register(JWTToken)
class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at')
    search_fields = ('user__username',)
"""
