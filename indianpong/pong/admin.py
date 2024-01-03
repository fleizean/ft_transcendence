from django.contrib import admin
from .models import UserProfile, Tournament, TournamentMatch, TwoFactorAuth, JWTToken, OAuthToken
from django.utils.html import format_html

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
    ('User Information', {'fields': ('username', 'password', 'displayname', 'email', 'avatar', 'friends' )}),
    ('Dates', {'fields': ('date_joined', 'last_login')}),
    ('Roles', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    ('Permissions', {'fields': ('groups', 'user_permissions')}),
    ('Stats', {'fields': ('wins', 'losses')}),
    )

    def avatar_thumbnail(self, obj):
        return format_html(obj.thumbnail)
    avatar_thumbnail.short_description = 'Avatar'
    

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date')
    search_fields = ('name',)

class TournamentMatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username', 'winner__username')

class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled')
    search_fields = ('user__username',)

class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at')
    search_fields = ('user__username',)

class OAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'refresh_token', 'expires_at')
    search_fields = ('user__username',)

admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.register(MatchHistory)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentMatch, TournamentMatchAdmin)
admin.site.register(TwoFactorAuth, TwoFactorAuthAdmin)
admin.site.register(JWTToken, JWTTokenAdmin)
admin.site.register(OAuthToken, OAuthTokenAdmin)
