from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import BlockUserForm, ChatMessageForm, InviteToGameForm, UserProfileForm, UpdateProfileForm, TwoFactorAuthSetupForm, JWTTokenForm, AuthenticationUserForm, TournamentForm, TournamentMatchForm, OAuthTokenForm
from .models import BlockedUser, ChatMessage, GameWarning, UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken
from .utils import pass2fa
from os import environ
import requests


def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Perform additional actions if needed
            login(request, user)  # Log in the user after successful registration
            return redirect('profile')
    else:
        form = UserProfileForm()
    return render(request, 'signup.html', {'form': form})

#2020-07-10 15:00:00.000
def auth(request):
	if request.user.is_authenticated:
		return redirect("index")
	if request.method == "GET":
		code = request.GET.get("code")
		if code:
			data = {
				"grant_type": "authorization_code",
				"client_id": environ.get("FT_CLIENT_ID"),
				"client_secret": environ.get("FT_CLIENT_SECRET"),
				"code": code,
				"redirect_uri": "http://127.0.0.1:8000/auth",
			}
			auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
			access_token = auth_response.json()["access_token"]
			user_response = requests.get("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
			username = user_response.json()["login"]
			display_name = user_response.json()["displayname"]

			try:
				user = UserProfile.objects.get(username=username)
				return pass2fa(request, user)
			except UserProfile.DoesNotExist:
				user = UserProfile.objects.create_user(username=username, display_name=display_name)
				login(request, user)
		else:
			messages.info(request, "Invalid authorization code")
			return redirect("login")
	else:
		messages.info(request, "Invalid method")
		return redirect("login")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationUserForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationUserForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url="login")
def logout_view(request):
	logout(request)
	return redirect("login")

@login_required
def chat_room(request):
    return render(request, 'chat_room.html')

@login_required
def chat(request):
    messages_sent = ChatMessage.objects.filter(sender=request.user)
    messages_received = ChatMessage.objects.filter(receiver=request.user)
    context = {'messages_sent': messages_sent, 'messages_received': messages_received}
    return render(request, 'chat.html', context)

@login_required
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

@login_required
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

@login_required
def unblock_user(request, blocked_user_id):
    blocked_user = UserProfile.objects.get(id=blocked_user_id)
    BlockedUser.objects.filter(user=request.user, blocked_user=blocked_user).delete()
    messages.success(request, f'You have unblocked {blocked_user.username}.')
    return redirect('chat')

@login_required
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

@login_required
def game_warning(request, opponent_id):
    opponent = UserProfile.objects.get(id=opponent_id)
    GameWarning.objects.create(user=request.user, opponent=opponent)
    messages.warning(request, f'Game warning sent to {opponent.username}.')
    return redirect('chat')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def setup_two_factor_auth(request):
    if request.method == 'POST':
        form = TwoFactorAuthSetupForm(request.POST, instance=request.user.twofactorauth)
        if form.is_valid():
            form.save()
            messages.success(request, 'Two-Factor Authentication successfully set up.')
            return redirect('profile')
    else:
        form = TwoFactorAuthSetupForm(instance=request.user.twofactorauth)
    return render(request, 'setup_two_factor_auth.html', {'form': form})

@login_required
def generate_jwt_token(request):
    if request.method == 'POST':
        form = JWTTokenForm(request.POST, instance=request.user.jwttoken)
        if form.is_valid():
            form.save()
            messages.success(request, 'JWT Token generated successfully.')
            return redirect('profile')
    else:
        form = JWTTokenForm(instance=request.user.jwttoken)
    return render(request, 'generate_jwt_token.html', {'form': form})

@login_required
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

@login_required
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



