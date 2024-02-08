import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .forms import (
    BlockUserForm,
    ChatMessageForm,
    DeleteAccountForm,
    InviteToGameForm,
    PasswordChangeUserForm,
    PasswordResetUserForm,
    SetPasswordUserForm,
    SocialForm,
    UserProfileForm,
    UpdateUserProfileForm,
    TwoFactorAuthSetupForm,
    JWTTokenForm,
    AuthenticationUserForm,
    TournamentForm,
    TournamentMatchForm,
)
from .models import (
    BlockedUser,
    ChatMessage,
    GameWarning,
    VerifyToken,
    UserProfile,
    TwoFactorAuth,
    JWTToken,
    Tournament,
    TournamentMatch,
    OAuthToken,
    Room,
    Message,
)
from .utils import pass2fa
from os import environ
from datetime import datetime, timedelta
from django.utils.http import urlsafe_base64_decode
import urllib.parse
import urllib.request
from urllib.parse import urlencode
import secrets, json, re
from django.core.files import File
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string
from django.urls import reverse



### Homepage and Error Page ###


@never_cache
def index(request):
    return render(request, "base.html")


@login_required(login_url="login")
def aboutus(request):
    return render(request, "aboutus.html")


def handler404(request, exception):
    return render(request, "404.html", status=404)


### User Authentication ###
@never_cache
def signup(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            obj = VerifyToken.objects.create(
                user=user, token=default_token_generator.make_token(user)
            )
            obj.send_verification_email(request, user)
            messages.success(request, "Please check your email to verify your account.")
            return HttpResponseRedirect("login?status=success")
    else:
        form = UserProfileForm()
    return render(request, "signup.html", {"form": form})


@never_cache
def activate_account(request, token):
    try:
        token = VerifyToken.objects.get(token=token)
    except VerifyToken.DoesNotExist:
        return render(request, "activation_fail.html")
    token.user.is_verified = True
    token.user.save()
    token.delete()
    messages.success(request, "Your account has been verified.")
    login(request, token.user)
    return redirect("profile", request.user.username)


# state_req = secrets.token_hex(25)
@never_cache
def auth(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    auth_url = "https://api.intra.42.fr/oauth/authorize"
    fields = {
        "client_id": "u-s4t2ud-4b7a045a7cc7dd977eeafae807bd4947670f273cb30e1dd674f6bfa490ba6c45",  # environ.get("FT_CLIENT_ID"),
        "redirect_uri": "http://localhost:8000/auth_callback",  # This should be parameterized
        "scope": "public",
        # "state": state_req,  # This will generate a 50-character long random string
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
            "client_id": "u-s4t2ud-4b7a045a7cc7dd977eeafae807bd4947670f273cb30e1dd674f6bfa490ba6c45",  # environ.get("FT_CLIENT_ID"),
            "client_secret": "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",  # environ.get("FT_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": "http://localhost:8000/auth_callback",
        }
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(
            "https://api.intra.42.fr/oauth/token", data=encoded_data
        )
        response = urllib.request.urlopen(req)

    # Process the response, store the access token, and authenticate the user
    if response.status == 200:
        token_data = json.loads(response.read().decode("utf-8"))
        """with open('token_data.json', 'w') as file:
            json.dump(token_data, file)"""
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        created_at = token_data.get("created_at")
        secret_valid_until = token_data.get("secret_valid_until")

        # Fetch user information from 42 API
        headers = {"Authorization": f"Bearer {access_token}"}
        req = urllib.request.Request("https://api.intra.42.fr/v2/me", headers=headers)
        user_info_response = urllib.request.urlopen(req)

        if user_info_response.status == 200:
            user_data = json.loads(user_info_response.read().decode("utf-8"))
            """with open('user_data.json', 'w') as file:
                json.dump(user_data, file) """

            # Create or get the user based on the 42 user ID
            user, created = UserProfile.objects.get_or_create(email=user_data["email"])
            if created:
                user.set_unusable_password()

                # Update user profile
                # add random string to username if it already exists
                if UserProfile.objects.filter(username=user_data["login"]).exists():
                    user.username = user_data["login"] + get_random_string(length=3)
                else:
                    user.username = user_data["login"]
                user.displayname = user_data.get("displayname", "")
                user.is_verified = True

                image_url = (
                    user_data.get("image", {}).get("versions", {}).get("medium", "")
                )
                if image_url:
                    image_name, response = urllib.request.urlretrieve(image_url)
                    print(image_name)
                    user.avatar.save(
                        f"{user.username}.jpg",
                        File(open(image_name, "rb")),
                        save=True,
                    )
                user.save()

                # Store the access token in the OAuthToken model
                oauth_token = OAuthToken.objects.create(
                    user=user,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_in=expires_in,
                    created_at=created_at,
                    secret_valid_until=secret_valid_until,
                )
                oauth_token.save()

            # Log in the user
            login(request, user)
            return redirect("dashboard")

    return redirect("login")  # Handle authentication failure


### Login and Logout ###


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("dashboard?status=success")
    valid = True
    toast_message = ""
    if request.method == "POST":
        form = AuthenticationUserForm(request, request.POST)
        if form.is_valid():

            user = form.get_user()
            """  if not user.is_verified:
                messages.error(request, "Account not verified")
                return redirect('login') """

            login(request, user)
            return HttpResponseRedirect("dashboard?status=success")
        else:
            valid = False  # şifre yanlışsa
            toast_message = "Username or password incorrectly"
    else:
        form = AuthenticationUserForm()
    return render(
        request,
        "login.html",
        {"form": form, "valid": valid, "toast_message": toast_message},
    )


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

    # try:
    #    profile = UserProfile.objects.get(username=username)
    # except UserProfile.DoesNotExist:
    # Render custom 404 page
    #    return render(request, '404.html', {'username': username}, status=404)

    profile = get_object_or_404(UserProfile, username=username)
    return render(request, "profile.html", {"profile": profile})


## Rps Game ##
@never_cache
@login_required(login_url="login")
def rps_game_find(request):
    return render(request, "rps-game-find.html")


## Pong Game ##
@never_cache
@login_required(login_url="login")
def pong_game_find(request):
    return render(request, "pong-game-find.html")


### Profile Settings ###
@never_cache
@login_required(login_url="login")
def profile_settings(request, username):
    if request.user.username != username:
        return redirect(reverse('profile_settings', kwargs={'username': request.user.username}))
    profile_form = UpdateUserProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    password_form = PasswordChangeUserForm(request.user, request.POST or None)
    social_form = SocialForm(request.POST or None, instance=request.user.social)
    delete_account_form = DeleteAccountForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if "profile_form" in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect(reverse('profile_settings', args=[username]) + '#editProfile')
        elif "password_form" in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect(reverse('profile_settings', args=[username]) + '#changePassword')
        elif "social_form" in request.POST:
            if social_form.is_valid():
                social = social_form.save(commit=False)
                social.user = request.user
                social.save()
                messages.success(request, "Socials updated successfully.")
                return redirect(reverse('profile_settings', args=[username]) + '#addSocial')
        elif "delete_account_form" in request.POST:
            if delete_account_form.is_valid():
                request.user.delete()
                logout(request)
                return redirect('')
    else:
        profile_form = UpdateUserProfileForm(instance=request.user)
        password_form = PasswordChangeUserForm(request.user)
        social_form = SocialForm(instance=request.user.social)
        delete_account_form = DeleteAccountForm(user=request.user)

    profile = get_object_or_404(UserProfile, username=username)
    return render(
        request,
        "profile-settings.html",
        {
            "profile": profile,
            "profile_form": profile_form,
            "password_form": password_form,
            "social_form": social_form,
            "delete_account_form": delete_account_form,
        },
    )

@never_cache
@login_required(login_url="login")
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeUserForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, "Password changed successfully.")
            return redirect("profile", request.user.username)
    else:
        form = PasswordChangeUserForm(request.user)
    return render(request, "password_change.html", {"form": form})


@never_cache
def password_reset(request):
    if request.method == "POST":
        form = PasswordResetUserForm(request.POST or None)
        if form.is_valid():
            # uid, token = form.save()
            form.save(request=request)
            # Perform additional actions if needed
            messages.success(request, "Password reset email sent successfully.")
            return redirect("password_reset_done")
            # return redirect('set_password', uidb64=uid, token=token)
    else:
        form = PasswordResetUserForm()
    return render(request, "password_reset.html", {"form": form})


@never_cache
def password_reset_done(request):
    return render(request, "password_reset_done.html")


@never_cache
def set_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # token is valid, you can show the user a form to enter a new password
        if request.method == "POST":
            form = SetPasswordUserForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset.")
                return redirect("login")
        else:
            form = SetPasswordUserForm(user)
        return render(request, "set_password.html", {"form": form})
    else:
        # invalid token
        messages.error(request, "The reset password link is invalid.")
        return redirect("password_reset")


""" @never_cache
@login_required(login_url="login")
def password_reset_done(request, uidb64, token):
    if request.method == 'POST':
        form = TokenValidationForm(request.POST)
        if form.is_valid():
            user_id = force_text(urlsafe_base64_decode(uidb64))
            #user = UserProfile.objects.get(pk=user_id)
            return redirect('set_password', uidb64, token)
    else:
        form = TokenValidationForm()
    return render(request, 'password_reset_done.html', {'form': form})

@never_cache
@login_required(login_url="login")
def set_password(request, uidb64, token):
    if request.method == 'POST':
        form = SetPasswordUserForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Perform additional actions if needed
            messages.success(request, 'Password set successfully.')
            return redirect('profile', request.user.username)
    else:
        form = SetPasswordUserForm()
    return render(request, 'set_password.html', {'form': form}) """

### Navbar ###


@never_cache
@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html")


@never_cache
@login_required(login_url="login")
def rankings(request):
    return render(request, "rankings.html")


@login_required(login_url="login")
def search(request):
    if request.method == "POST":
        search_query = request.POST.get("search_query", "")
        if len(search_query) >= 3:
            email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            if re.fullmatch(email_regex, search_query):
                results = UserProfile.objects.filter(
                    Q(username__icontains=search_query)
                    | Q(email__icontains=search_query)
                )
            else:
                results = UserProfile.objects.filter(username__icontains=search_query)
            return render(request, "search.html", {"results": results})
    return render(request, "search.html")


@login_required(login_url="login")
def game(request):
    return render(request, "game.html")


@never_cache
@login_required(login_url="login")
def chat(request):
    users = UserProfile.objects.all().exclude(username=request.user)
    return render(request, "chat.html", {"users": users})


@login_required(login_url="login")
def aboutus(request):
    return render(request, "aboutus.html")


@login_required(login_url="login")
def friends(request, profile):
    profile = get_object_or_404(UserProfile, username=profile)
    friends = profile.friends.all()
    return render(request, "friends.html", {"friends": friends, "profile": profile})


@login_required(login_url="login")
def match_history(request, profile):
    profile = get_object_or_404(UserProfile, username=profile)

    return render(request, "match-history.html", {"profile": profile})


### New Chat ###
@login_required(login_url="login")
def room(request, room_name):
    users = UserProfile.objects.all().exclude(username=request.user)
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)
    return render(
        request,
        "room.html",
        {
            "room_name": room_name,
            "room": room,
            "users": users,
            "messages": messages,
        },
    )


@login_required(login_url="login")
def start_chat(request, username):
    second_user = UserProfile.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except Room.DoesNotExist:
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect("room", room.id)


### OldChat ###


@never_cache
@login_required(login_url="login")
def chat_room(request):
    messages_sent = ChatMessage.objects.filter(sender=request.user)
    messages_received = ChatMessage.objects.filter(receiver=request.user)
    context = {"messages_sent": messages_sent, "messages_received": messages_received}
    return render(request, "chat_room.html", context)


@never_cache
@login_required(login_url="login")
def send_message(request, receiver_id):
    receiver = UserProfile.objects.get(id=receiver_id)
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, "Message sent successfully.")
            return redirect("chat")
    else:
        form = ChatMessageForm()
    context = {"form": form, "receiver": receiver}
    return render(request, "send_message.html", context)


@never_cache
@login_required(login_url="login")
def block_user(request):
    if request.method == "POST":
        form = BlockUserForm(request.POST)
        if form.is_valid():
            blocked_user = form.cleaned_data["blocked_user"]
            blocking_relation, created = BlockedUser.objects.get_or_create(
                user=request.user, blocked_user=blocked_user
            )
            if created:
                messages.success(request, f"You have blocked {blocked_user.username}.")
            else:
                messages.warning(
                    request, f"You have already blocked {blocked_user.username}."
                )
            return redirect("chat")
    else:
        form = BlockUserForm()
    return render(request, "block_user.html", {"form": form})


@never_cache
@login_required(login_url="login")
def unblock_user(request, blocked_user_id):
    blocked_user = UserProfile.objects.get(id=blocked_user_id)
    BlockedUser.objects.filter(user=request.user, blocked_user=blocked_user).delete()
    messages.success(request, f"You have unblocked {blocked_user.username}.")
    return redirect("chat")


@never_cache
@login_required(login_url="login")
def invite_to_game(request, invited_user_id):
    invited_user = UserProfile.objects.get(id=invited_user_id)
    if request.method == "POST":
        form = InviteToGameForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.inviting_user = request.user
            invitation.invited_user = invited_user
            invitation.save()
            messages.success(
                request, f"Invitation sent to {invited_user.username} successfully."
            )
            return redirect("chat")
    else:
        form = InviteToGameForm()
    context = {"form": form, "invited_user": invited_user}
    return render(request, "invite_to_game.html", context)


@never_cache
@login_required(login_url="login")
def game_warning(request, opponent_id):
    opponent = UserProfile.objects.get(id=opponent_id)
    GameWarning.objects.create(user=request.user, opponent=opponent)
    messages.warning(request, f"Game warning sent to {opponent.username}.")
    return redirect("chat")


### Tournaments ###


@never_cache
@login_required(login_url="login")
def create_tournament(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            messages.success(
                request, f'Tournament "{tournament.name}" created successfully.'
            )
            return redirect("tournament_list")
    else:
        form = TournamentForm()
    return render(request, "create_tournament.html", {"form": form})


@never_cache
@login_required(login_url="login")
def create_tournament_match(request):
    if request.method == "POST":
        form = TournamentMatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            messages.success(
                request,
                f"Match between {match.player1} and {match.player2} created successfully.",
            )
            return redirect("tournament_match_list")
    else:
        form = TournamentMatchForm()
    return render(request, "create_tournament_match.html", {"form": form})


### Two-Factor Authentication ###


@never_cache
@login_required(login_url="login")
def setup_two_factor_auth(request):
    if request.method == "POST":
        form = TwoFactorAuthSetupForm(request.POST, instance=request.user.twofactorauth)
        if form.is_valid():
            form.save()

            messages.success(request, "Two-Factor Authentication successfully set up.")
            return redirect("profile", request.user.username)
    else:
        form = TwoFactorAuthSetupForm(instance=request.user.twofactorauth)
    return render(request, "setup_two_factor_auth.html", {"form": form})


@never_cache
@login_required(login_url="login")
def generate_jwt_token(request):
    if request.method == "POST":
        form = JWTTokenForm(request.POST, instance=request.user.jwttoken)
        if form.is_valid():
            form.save()
            messages.success(request, "JWT Token generated successfully.")
            return redirect("profile", request.user.username)
    else:
        form = JWTTokenForm(instance=request.user.jwttoken)
    return render(request, "generate_jwt_token.html", {"form": form})
