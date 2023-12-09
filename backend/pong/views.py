from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserProfileForm, UpdateProfileForm, TwoFactorAuthSetupForm, JWTTokenForm, AuthenticationUserForm, TournamentForm, TournamentMatchForm, OAuthTokenForm
from .models import UserProfile, TwoFactorAuth, JWTToken, Tournament, TournamentMatch, OAuthToken

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



