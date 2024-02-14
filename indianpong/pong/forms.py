from datetime import timedelta
from email.mime.image import MIMEImage
import os
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from indianpong.settings import EMAIL_HOST_USER, STATICFILES_DIRS
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm 
from .models import Social, VerifyToken, BlockedUser, ChatMessage, GameInvitation, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch

class UserProfileForm(UserCreationForm):

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    displayname = forms.CharField(label='Displayname', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='RePassword', widget=forms.PasswordInput(attrs={'class': 'input'}))
    #avatar = forms.ImageField(required=False ,label='Avatar', widget=forms.FileInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'displayname', 'email', 'password1', 'password2']

    """ def confirm_login_allowed(self, user):
        if not user.is_verified:
            raise forms.ValidationError(
                mark_safe(
                    "This account is not verified. <a href='{}'>Resend verification email</a>".format(
                        reverse("password_reset")
                    )
                )
            ) """

    def clean_email(self): #TODO not just 42kocaeli.com.tr
        email = self.cleaned_data.get('email')

        if "@student.42" in email:
            raise forms.ValidationError('Use 42 login')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isascii():
            raise forms.ValidationError("Username cannot contain non-ASCII characters.")
        return username
    
class StoreItemActionForm(forms.Form):
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('equip', 'Equip'),
        ('customize', 'Customize'),
    ]
    name = forms.CharField(max_length=200, required=False)
    action = forms.ChoiceField(choices=ACTION_CHOICES)
    whatis = forms.CharField(max_length=200, required=False)

class SocialForm(forms.ModelForm):
    stackoverflow = forms.CharField(label='Stackoverflow', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    twitter = forms.CharField(label='Twitter', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    instagram = forms.CharField(label='Instagram', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    github = forms.CharField(label='Github', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Social
        fields = ['stackoverflow', 'twitter', 'instagram', 'github']

class DeleteAccountForm(forms.Form):
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Enter your password to confirm account deletion.")
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}), help_text="Enter your email to confirm account deletion.")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DeleteAccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not self.user.email == email:
            raise forms.ValidationError("Email does not match")
        return cleaned_data

class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

class UpdateUserProfileForm(UserChangeForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    displayname = forms.CharField(label='Displayname', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #password = forms.CharField(widget=forms.HiddenInput(), required=False, help_text="")
    password = None
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'displayname']
        #exclude = ['password']

class ProfileAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['avatar']

class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='ReNew Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['old_password', 'new_password1', 'new_password2']

class PasswordResetUserForm(PasswordResetForm):
    #email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    
    """    class Meta:
        model = UserProfile
        fields = ['email'] """

    def save(self, domain_override=None, token_generator=default_token_generator, request=None):
        email = self.cleaned_data["email"]
        # check if user exists with given email
        user = UserProfile.objects.filter(email=email).first()
        if user is None:
            self.add_error('email', 'User does not exist with this email.')
            return
        token = token_generator.make_token(user)
        VerifyToken.objects.create(user=user, token=token)
        mail_subject = 'Reset your password'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'domain': domain_override or request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })

        
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,  # this is the simple text version
            from_email=EMAIL_HOST_USER,
            to=[user.email]
        )

        # Add the HTML version. This could be the same as the body if your email is only HTML.
        email.attach_alternative(message, "text/html")

        # List of images
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
            email.attach(img)

        # Send the email
        email.send(fail_silently=True)
        #send_mail(mail_subject, message, EMAIL_HOST_USER, [user.email], fail_silently=True, html_message=message)


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


