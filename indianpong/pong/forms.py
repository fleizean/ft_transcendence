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
from .models import Social, VerifyToken, BlockedUser, ChatMessage, GameInvitation, UserProfile, TwoFactorAuth, JWTToken, Tournament


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

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang', 'en')  # Varsayılan dil: İngilizce
        super().__init__(*args, **kwargs)

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
        lang = self.lang

        if "@student.42" in email:
            if (lang == 'tr'):
                raise forms.ValidationError('42 email adresi kullanamazsiniz')
            elif (lang == 'en'):
                raise forms.ValidationError('Cannot use 42 email address')
            elif (lang == 'hi'):
                raise forms.ValidationError('42 ईमेल पता नहीं उपयोग कर सकते')
            elif (lang == 'pt'):
                raise forms.ValidationError('Não é possível usar o endereço de e-mail 42')
            else:
                raise forms.ValidationError('Cannot use 42 email address')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        displayname = self.cleaned_data.get("displayname")
        lang = self.lang
        if not username:
            if (lang == 'tr'):
                raise forms.ValidationError("Kullanici adi zorunludur.")
            elif (lang == 'en'):
                raise forms.ValidationError("Username is required.")
            elif (lang == 'hi'):
                raise forms.ValidationError("उपयोगकर्ता नाम आवश्यक है।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Nome de usuário é obrigatório.")
            else:
                raise forms.ValidationError("Username is required.")
        if not username.isascii():
            if (lang == 'tr'):
                raise forms.ValidationError("Kullanici adi ASCII olmayan karakterler icermemelidir.")
            elif (lang == 'en'):
                raise forms.ValidationError("Username cannot contain non-ASCII characters.")
            elif (lang == 'hi'):
                raise forms.ValidationError("उपयोगकर्ता नाम में अशी नहीं हो सकते।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Nome de usuário não pode conter caracteres não ASCII.")
            else:
                raise forms.ValidationError("Username cannot contain non-ASCII characters.")
        
        if username == displayname:
            if (lang == 'tr'):
                raise forms.ValidationError("Kullanıcı adı ve gorunen ad ayni olamaz.")
            elif (lang == 'en'):
                raise forms.ValidationError("Username and displayname cannot be the same.")
            elif (lang == 'hi'):
                raise forms.ValidationError("उपयोगकर्ता नाम और प्रदर्शन नाम एक ही नहीं हो सकते।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Nome de usuário e nome de exibicão não podem ser iguais.")
            else:
                raise forms.ValidationError("Username and displayname cannot be the same.")
        return username

    def clean_displayname(self):
        displayname = self.cleaned_data.get("displayname")
        username = self.cleaned_data.get("username")
        lang = self.lang
        
        if not displayname:
            if (lang == 'tr'):
                raise forms.ValidationError("Gorunen ad zorunludur.")
            elif (lang == 'en'):
                raise forms.ValidationError("Displayname is required.")
            elif (lang == 'hi'):
                raise forms.ValidationError("प्रदर्शन नाम आवश्यक है।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Nome de exibicão é obrigatório.")
            else:
                raise forms.ValidationError("Displayname is required.")
        if username == displayname:
            if (lang == 'tr'):
                raise forms.ValidationError("Kullanıcı adı ve gorunen ad ayni olamaz.")
            elif (lang == 'en'):
                raise forms.ValidationError("Username and displayname cannot be the same.")
            elif (lang == 'hi'):
                raise forms.ValidationError("उपयोगकर्ता नाम और प्रदर्शन नाम एक ही नहीं हो सकते।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Nome de usuário e nome de exibicão não podem ser iguais.")
            else:
                raise forms.ValidationError("Username and displayname cannot be the same.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        lang = self.lang
        if not email:
            if (lang == 'tr'):
                raise forms.ValidationError("Email zorunludur.")
            elif (lang == 'en'):
                raise forms.ValidationError("Email is required.")
            elif (lang == 'hi'):
                raise forms.ValidationError("ईमेल आवश्यक है।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Email é obrigatório.")
            else:
                raise forms.ValidationError("Email is required.")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        lang = self.lang
        if not password1:
            if (lang == 'tr'):
                raise forms.ValidationError("Parola zorunludur.")
            elif (lang == 'en'):
                raise forms.ValidationError("Password is required.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड आवश्यक है।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Senha é obrigatória.")
            else:
                raise forms.ValidationError("Password is required.")
        
        if len(password1) < 8:
            if (lang == 'tr'):
                raise forms.ValidationError("Parola en az 8 karakter uzunlugunda olmalidir.")
            elif (lang == 'en'):
                raise forms.ValidationError("Password must be at least 8 characters long.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड कम से कम 8 वर्ण लंबा होना चाहिए।")
            elif (lang == 'pt'):
                raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
            else:
                raise forms.ValidationError("Password must be at least 8 characters long.")

        if not any(char.isdigit() for char in password1):
            if (lang == 'tr'):
                raise forms.ValidationError("Parola en az bir rakam içermelidir.")
            elif (lang == 'en'):
                raise forms.ValidationError("Password must contain at least one digit.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड में कम से कम एक अंक होना चाहिए।")
            elif (lang == 'pt'):
                raise forms.ValidationError("A senha deve conter pelo menos um dígito.")
            else:
                raise forms.ValidationError("Password must contain at least one digit.")
        
        
        if not any(char.isalpha() for char in password1):
            if (lang == 'tr'):
                raise forms.ValidationError("Parola en az bir harf içermelidir.")
            elif (lang == 'en'):
                raise forms.ValidationError("Password must contain at least one letter.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड में कम से कम एक अक्षर होना चाहिए।")
            elif (lang == 'pt'):
                raise forms.ValidationError("A senha deve conter pelo menos uma letra.")
            else:
                raise forms.ValidationError("Password must contain at least one letter.")

        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        lang = self.lang

        if not password2:
            if (lang == 'tr'):
                raise forms.ValidationError("Parolayi tekrar girmek zorunludur.")
            elif (lang == 'en'):
                raise forms.ValidationError("Re-entering password is required.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड फिर से दर्ज करना आवश्यक है।")
            elif (lang == 'pt'):
                raise forms.ValidationError("Re-entrar senha é obrigatório.")
            else:
                raise forms.ValidationError("Re-entering password is required.")

        if password1 != password2:
            if (lang == 'tr'):
                raise forms.ValidationError("Parolalar eslesmiyor.")
            elif (lang == 'en'):
                raise forms.ValidationError("Passwords do not match.")
            elif (lang == 'hi'):
                raise forms.ValidationError("पासवर्ड मेल नहीं खा रहे हैं।")
            elif (lang == 'pt'):
                raise forms.ValidationError("As senhas não coincidem.")
            else:
                raise forms.ValidationError("Passwords do not match.")
        return password2
    
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        lang = self.lang
        if avatar:
            if avatar.size > 2*1024*1024:
                error_message = {
                    'tr': "Resim dosya boyutu 2MB'dan az olmalidir.",
                    'en': "Image file size should be less than 2MB",
                    'hi': "छवि फ़ाइल का आकार 2MB से कम होना चाहिए",
                    'pt': "O tamanho do arquivo de imagem deve ser inferior a 2MB",
                    # Diğer diller için gerekli hata mesajlarını ekleyin
                }
                raise forms.ValidationError(error_message.get(lang, "Image file size should be less than 2MB")) 

            return avatar
    
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
    intra42 = forms.CharField(label='Intra42', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    linkedin = forms.CharField(label='Linkedin', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    github = forms.CharField(label='Github', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    twitter = forms.CharField(label='Twitter', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Social
        fields = ['intra42', 'linkedin', 'github', 'twitter']

class DeleteAccountForm(forms.Form):
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Enter your password to confirm account deletion.")
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

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


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'max_score', 'game_mode']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TournamentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        # Call the original save method
        tournament = super(TournamentForm, self).save(commit=False, *args, **kwargs)
        
        # Assign the creator field to the user who sent the form
        tournament.creator = self.request.user

        # Save the changes
        if commit:
            tournament.save()
            # Add the creator to the participants list
            tournament.participants.add(self.request.user)
        return tournament
    

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





