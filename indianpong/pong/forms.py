# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import BlockedUser, ChatMessage, GameInvitation, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken

class UserProfileForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'displayname', 'email', 'password1', 'password2', 'avatar']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class BlockUserForm(forms.ModelForm):
    blocked_user = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = BlockedUser
        fields = ['blocked_user']

class InviteToGameForm(forms.ModelForm):
    invited_user = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = GameInvitation
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class UpdateProfileForm(forms.ModelForm):
    #avatar = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']

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

"""     def savem2m(self):
        pass """


