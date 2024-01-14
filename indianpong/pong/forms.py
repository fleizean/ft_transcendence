# forms.py
from datetime import timedelta
from django import forms
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm 
from .models import VerifyToken, BlockedUser, ChatMessage, GameInvitation, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken

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
    #email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    
    """    class Meta:
        model = UserProfile
        fields = ['email'] """

    def save(self, domain_override=None, subject_template_name=None,
            email_template_name=None, use_https=False, token_generator=default_token_generator,
            from_email=None, request=None, html_email_template_name=None, extra_email_context=None):
        super().save(request=request, token_generator=token_generator, use_https=use_https)
        token = token_generator.make_token(request.user)
        VerifyToken.objects.create(user=request.user, token=token)
        mail_subject = 'Reset your password'
        message = render_to_string('password_reset_email.html', {
            'user': request.user,
            'domain': domain_override or request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'token': token,
        })
        send_mail(mail_subject, message, 'noreply@indianpong.com', [request.user.email])
        #return uid, token

""" class TokenValidationForm(forms.Form):
    token = forms.CharField(label='Token', widget=forms.TextInput(attrs={'class': 'input'}) )

    class Meta:
        model = Token
        fields = ['token']

    def clean_token(self):
        token = self.cleaned_data.get('token')
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj or timezone.now() - token_obj.created_at > timedelta(minutes=2):
            raise forms.ValidationError('Invalid or expired token.')
        return token """

#After reset password
class SetPasswordUserForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(label='ReNew Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    
    class Meta:
        model = UserProfile
        fields = ['new_password1', 'new_password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            VerifyToken.objects.filter(user=user).delete()
        return user

    

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
        fields = ['name']

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


