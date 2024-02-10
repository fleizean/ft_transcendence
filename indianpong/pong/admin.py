from django.contrib import admin
from .models import OAuthToken, Social, UserItem, StoreItem, UserProfile, Tournament, Room, Message
from django.utils.html import format_html

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin class for managing user profiles.

    Attributes:
        list_display (tuple): A tuple of fields to be displayed in the admin list view.
        search_fields (tuple): A tuple of fields to be used for searching in the admin list view.
        fieldsets (tuple): A tuple of fieldsets to be displayed in the admin edit view.
    """

    list_display = ('username', 'email', 'displayname', 'avatar_thumbnail', 'wins', 'losses')
    search_fields = ('username', 'email', 'displayname')
    fieldsets = (
    ('User Information', {'fields': ('username', 'password', 'displayname', 'email', 'avatar', 'friends', 'is_42student')}),
    ('Dates', {'fields': ('date_joined', 'last_login')}),
    ('Roles', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified')}),
    ('Permissions', {'fields': ('groups', 'user_permissions')}),
    ('Stats', {'fields': ('wins', 'losses')}),
    )

    def avatar_thumbnail(self, obj):
        return format_html(obj.thumbnail)
    avatar_thumbnail.short_description = 'Avatar'

@admin.register(StoreItem)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_url', 'description', 'price', 'is_bought', 'is_status')
    search_fields = ('name', 'description')

@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'is_equipped')
    list_filter = ('is_equipped',)
    search_fields = ('user__username', 'item__name')

@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'stackoverflow', 'github', 'twitter', 'instagram')

    def get_user(self, obj):
        return obj.userprofile
    get_user.short_description = 'User'

    search_fields = ('userprofile__username', 'stackoverflow', 'github', 'twitter', 'instagram')
    
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date')
    search_fields = ('name',)

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

""" @admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled')
    search_fields = ('user__username',)

@admin.register(JWTToken)
class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at')
    search_fields = ('user__username',)
"""
