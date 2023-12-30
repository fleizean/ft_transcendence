from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MatchHistory, Tournament, TournamentMatch, TwoFactorAuth, JWTToken, OAuthToken


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'displayname','wins', 'losses')
    search_fields = ('username', 'email', 'displayname')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('displayname', 'avatar', 'wins', 'losses')}),
    )

    def thumbnail(self, obj):
        return obj.thumbnail
    
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Avatar'
    

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
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
admin.site.register(MatchHistory)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentMatch, TournamentMatchAdmin)
admin.site.register(TwoFactorAuth, TwoFactorAuthAdmin)
admin.site.register(JWTToken, JWTTokenAdmin)
admin.site.register(OAuthToken, OAuthTokenAdmin)
