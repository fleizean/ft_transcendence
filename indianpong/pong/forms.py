# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm 
from .models import BlockedUser, ChatMessage, GameInvitation, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken

class UserProfileForm(UserCreationForm):

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    displayname = forms.CharField(label='Displayname', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='RePassword', widget=forms.PasswordInput(attrs={'class': 'input'}))
    avatar = forms.ImageField(required=False ,label='Avatar', widget=forms.FileInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'displayname', 'email', 'password1', 'password2', 'avatar']

class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

class UpdateUserProfileForm(UserChangeForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    displayname = forms.CharField(label='Displayname', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    avatar = forms.ImageField(required=False ,label='Avatar', widget=forms.FileInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'displayname', 'email', 'avatar']

""" class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    displayname = forms.CharField(label='Displayname', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    avatar = forms.ImageField(required=False ,label='Avatar', widget=forms.FileInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'displayname', 'email', 'avatar'] """


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(label='ReNew Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['old_password', 'new_password1', 'new_password2']

class PasswordResetUserForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['email']

#After reset password
class SetPasswordUserForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(label='ReNew Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    uidb64 = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'input'}))
    token = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['new_password1', 'new_password2']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class BlockUserForm(forms.ModelForm):
    blocked_user = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = BlockedUser
        fields = ['blocked_user']

class InviteToGameForm(forms.ModelForm):
    invited_user = forms.ModelChoiceField(queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = GameInvitation
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }


class TwoFactorAuthSetupForm(forms.ModelForm):
    class Meta:
        model = TwoFactorAuth
        fields = ['is_enabled']

class JWTTokenForm(forms.ModelForm):
    class Meta:
        model = JWTToken
        fields = ['token']


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


