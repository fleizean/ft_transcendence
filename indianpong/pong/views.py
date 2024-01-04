from urllib.request import urlretrieve
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .forms import BlockUserForm, ChatMessageForm, InviteToGameForm, PasswordChangeUserForm, PasswordResetUserForm, SetPasswordUserForm, UserProfileForm, UpdateUserProfileForm, TwoFactorAuthSetupForm, JWTTokenForm, AuthenticationUserForm, TournamentForm, TournamentMatchForm, OAuthTokenForm
from .models import BlockedUser, ChatMessage, GameWarning, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken
from .utils import pass2fa
from os import environ
from datetime import datetime, timedelta
import urllib.parse
import urllib.request
from urllib.parse import urlencode
import secrets, json
from django.core.files import File
import json


### Homepage and Error Page ###

@never_cache
def index(request):
    return render(request, 'base.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)

### User Authentication ###

@never_cache
def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Perform additional actions if needed
            login(request, user)  # Log in the user after successful registration
            return redirect('profile', request.user)
    else:
        form = UserProfileForm()
    return render(request, 'signup.html', {'form': form})

#state_req = secrets.token_hex(25)
@never_cache
def auth(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    auth_url = "https://api.intra.42.fr/oauth/authorize"
    fields = {       
        "client_id": "u-s4t2ud-4b7a045a7cc7dd977eeafae807bd4947670f273cb30e1dd674f6bfa490ba6c45",#environ.get("FT_CLIENT_ID"),
        "redirect_uri": "http://localhost:8000/auth_callback", # This should be parameterized
        "scope": "public",
        #"state": state_req,  # This will generate a 50-character long random string
        "response_type": "code",
    }
    encoded_params = urlencode(fields)
    url = f"{auth_url}?{encoded_params}"
    return redirect(url)

@never_cache
def auth_callback(request):
    # Handle the callback from 42 and exchange the code for an access token
    if request.method == "GET":
        code = request.GET.get("code")
        data = {
            "grant_type": "authorization_code",
            "client_id": "u-s4t2ud-4b7a045a7cc7dd977eeafae807bd4947670f273cb30e1dd674f6bfa490ba6c45",#environ.get("FT_CLIENT_ID"),
            "client_secret": "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",#environ.get("FT_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": "http://localhost:8000/auth_callback",
        }
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request("https://api.intra.42.fr/oauth/token", data=encoded_data)
        response = urllib.request.urlopen(req)

    # Process the response, store the access token, and authenticate the user
    if response.status == 200:
        token_data = json.loads(response.read().decode('utf-8'))
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')

        # Fetch user information from 42 API
        headers = {'Authorization': f'Bearer {access_token}'}
        req = urllib.request.Request('https://api.intra.42.fr/v2/me', headers=headers)
        user_info_response = urllib.request.urlopen(req)

        if user_info_response.status == 200:
            user_data = json.loads(user_info_response.read().decode('utf-8'))

            # Create or get the user based on the 42 user ID
            user, created = UserProfile.objects.get_or_create(username=user_data['login'])
            if created:
                user.set_unusable_password()

            # Update user profile
            profile, _ = UserProfile.objects.get_or_create(username=user.username)
            profile.displayname = user_data.get('displayname', '')
            profile.email = user_data.get('email', '')
            # ...

            # Fetch user information from 42 API
            headers = {'Authorization': f'Bearer {access_token}'}
            req = urllib.request.Request('https://api.intra.42.fr/v2/me', headers=headers)
            user_info_response = urllib.request.urlopen(req)

            if user_info_response.status == 200:
                user_data = json.loads(user_info_response.read().decode('utf-8'))

                # Create or get the user based on the 42 user ID
                user, created = UserProfile.objects.get_or_create(username=user_data['login'])
                if created:
                    user.set_unusable_password()

                # Update user profile
                profile, _ = UserProfile.objects.get_or_create(username=user.username)
                profile.displayname = user_data.get('displayname', '')
                profile.email = user_data.get('email', '')

                image_url = user_data.get('image_url', '')
                if image_url:
                    image_name, _ = urllib.request.urlretrieve(image_url)
                    profile.avatar.save(image_name.split('/')[-1], File(open(image_name, 'rb')), save=True)
                profile.save()

            # Store the access token in the OAuthToken model
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            oauth_token, _ = OAuthToken.objects.get_or_create(user=profile)
            oauth_token.access_token = access_token
            oauth_token.refresh_token = refresh_token
            oauth_token.expires_at = expires_at
            oauth_token.save()

            # Log in the user
            login(request, user)
            return redirect('dashboard')

    return redirect('login')  # Handle authentication failure

### Login and Logout ###

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationUserForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationUserForm()
    return render(request, 'login.html', {'form': form})

@never_cache
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


### Profile ###

""" @login_required(login_url="login")
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user}) """

@never_cache
@login_required(login_url="login")
def profile_view(request, username):
    #try:
    #    profile = UserProfile.objects.get(username=username)
    #except UserProfile.DoesNotExist:
        # Render custom 404 page
    #    return render(request, '404.html', {'username': username}, status=404)

    profile = get_object_or_404(UserProfile, username=username)
    return render(request, 'profile.html', {'profile': profile})

### Profile Settings ###

@never_cache
@login_required(login_url="login")
def update_profile(request):
    if request.method == 'POST':
        form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', request.user)
    else:
        form = UpdateUserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@never_cache
@login_required(login_url="login")
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeUserForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, 'Password changed successfully.')
            return redirect('profile', request.user)
    else:
        form = PasswordChangeUserForm(request.user)
    return render(request, 'password_change.html', {'form': form})

@never_cache
@login_required(login_url="login")
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, 'Password reset email sent successfully.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetUserForm()
    return render(request, 'password_reset.html', {'form': form})

@never_cache
@login_required(login_url="login")
def password_reset_done(request):
    return render(request, 'password_reset_done.html')

@never_cache
@login_required(login_url="login")
def set_password(request, uidb64, token):
    if request.method == 'POST':
        form = SetPasswordUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, 'Password set successfully.')
            return redirect('profile', request.user)
    else:
        form = SetPasswordUserForm()
    return render(request, 'set_password.html', {'form': form})

### Navbar ###

@never_cache
@login_required(login_url="login")
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

@never_cache
@login_required(login_url="login")
def rankings(request):
    return render(request, 'rankings.html', {'username': request.user.username})

@never_cache
@login_required(login_url="login")
def search(request):
    return render(request, 'search.html', {'username': request.user.username})


@login_required(login_url="login")
def game(request):
    request.user.status = "online"
    request.user.save()
    return render(request, 'sock.html', {'username': request.user.username})

@never_cache
@login_required(login_url="login")
def chat(request):
    return render(request, 'chat.html', {'username': request.user.username})


### Chat ###

@never_cache
@login_required(login_url="login")
def chat_room(request):
    messages_sent = ChatMessage.objects.filter(sender=request.user)
    messages_received = ChatMessage.objects.filter(receiver=request.user)
    context = {'messages_sent': messages_sent, 'messages_received': messages_received}
    return render(request, 'chat_room.html', context)

@never_cache
@login_required(login_url="login")
def send_message(request, receiver_id):
    receiver = UserProfile.objects.get(id=receiver_id)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('chat')
    else:
        form = ChatMessageForm()
    context = {'form': form, 'receiver': receiver}
    return render(request, 'send_message.html', context)

@never_cache
@login_required(login_url="login")
def block_user(request):
    if request.method == 'POST':
        form = BlockUserForm(request.POST)
        if form.is_valid():
            blocked_user = form.cleaned_data['blocked_user']
            blocking_relation, created = BlockedUser.objects.get_or_create(
                user=request.user,
                blocked_user=blocked_user
            )
            if created:
                messages.success(request, f'You have blocked {blocked_user.username}.')
            else:
                messages.warning(request, f'You have already blocked {blocked_user.username}.')
            return redirect('chat')
    else:
        form = BlockUserForm()
    return render(request, 'block_user.html', {'form': form})

@never_cache
@login_required(login_url="login")
def unblock_user(request, blocked_user_id):
    blocked_user = UserProfile.objects.get(id=blocked_user_id)
    BlockedUser.objects.filter(user=request.user, blocked_user=blocked_user).delete()
    messages.success(request, f'You have unblocked {blocked_user.username}.')
    return redirect('chat')

@never_cache
@login_required(login_url="login")
def invite_to_game(request, invited_user_id):
    invited_user = UserProfile.objects.get(id=invited_user_id)
    if request.method == 'POST':
        form = InviteToGameForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.inviting_user = request.user
            invitation.invited_user = invited_user
            invitation.save()
            messages.success(request, f'Invitation sent to {invited_user.username} successfully.')
            return redirect('chat')
    else:
        form = InviteToGameForm()
    context = {'form': form, 'invited_user': invited_user}
    return render(request, 'invite_to_game.html', context)

@never_cache
@login_required(login_url="login")
def game_warning(request, opponent_id):
    opponent = UserProfile.objects.get(id=opponent_id)
    GameWarning.objects.create(user=request.user, opponent=opponent)
    messages.warning(request, f'Game warning sent to {opponent.username}.')
    return redirect('chat')

### Tournaments ###

@never_cache
@login_required(login_url="login")
def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            messages.success(request, f'Tournament "{tournament.name}" created successfully.')
            return redirect('tournament_list')
    else:
        form = TournamentForm()
    return render(request, 'create_tournament.html', {'form': form})

@never_cache
@login_required(login_url="login")
def create_tournament_match(request):
    if request.method == 'POST':
        form = TournamentMatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            messages.success(request, f'Match between {match.player1} and {match.player2} created successfully.')
            return redirect('tournament_match_list')
    else:
        form = TournamentMatchForm()
    return render(request, 'create_tournament_match.html', {'form': form})

### Two-Factor Authentication ###

@never_cache
@login_required(login_url="login")
def setup_two_factor_auth(request):
    if request.method == 'POST':
        form = TwoFactorAuthSetupForm(request.POST, instance=request.user.twofactorauth)
        if form.is_valid():
            form.save()

            messages.success(request, 'Two-Factor Authentication successfully set up.')
            return redirect('profile', request.user)
    else:
        form = TwoFactorAuthSetupForm(instance=request.user.twofactorauth)
    return render(request, 'setup_two_factor_auth.html', {'form': form})

@never_cache
@login_required(login_url="login")
def generate_jwt_token(request):
    if request.method == 'POST':
        form = JWTTokenForm(request.POST, instance=request.user.jwttoken)
        if form.is_valid():
            form.save()
            messages.success(request, 'JWT Token generated successfully.')
            return redirect('profile', request.user)
    else:
        form = JWTTokenForm(instance=request.user.jwttoken)
    return render(request, 'generate_jwt_token.html', {'form': form})







