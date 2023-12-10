# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken

class UserProfileForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'display_name', 'password1', 'password2', 'avatar']

class UpdateProfileForm(forms.ModelForm):
    #avatar = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = ['display_name', 'avatar']

class TwoFactorAuthSetupForm(forms.ModelForm):
    class Meta:
        model = TwoFactorAuth
        fields = ['is_enabled']

class JWTTokenForm(forms.ModelForm):
    class Meta:
        model = JWTToken
        fields = ['token']

class AuthenticationUserForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date']

class TournamentMatchForm(forms.ModelForm):
    class Meta:
        model = TournamentMatch
        fields = ['tournament', 'player1', 'player2']

class OAuthTokenForm(forms.ModelForm):
    class Meta:
        model = OAuthToken
        fields = ['access_token', 'refresh_token', 'expires_at']


