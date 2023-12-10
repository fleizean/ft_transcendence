from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MatchHistory, Tournament, TournamentMatch, TwoFactorAuth, JWTToken, OAuthToken


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name', 'wins', 'losses')
    search_fields = ('username', 'email', 'display_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('display_name', 'avatar', 'wins', 'losses')}),
    )

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)

class TournamentMatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner')
    search_fields = ('tournament__name', 'player1__display_name', 'player2__display_name', 'winner__display_name')

class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled')
    search_fields = ('user__display_name',)

class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at')
    search_fields = ('user__display_name',)

class OAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'refresh_token', 'expires_at')
    search_fields = ('user__display_name',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MatchHistory)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentMatch, TournamentMatchAdmin)
admin.site.register(TwoFactorAuth, TwoFactorAuthAdmin)
admin.site.register(JWTToken, JWTTokenAdmin)
admin.site.register(OAuthToken, OAuthTokenAdmin)
