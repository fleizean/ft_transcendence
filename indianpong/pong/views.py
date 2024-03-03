import os
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ssl  # TODO temporary solution

from .forms import (
    BlockUserForm,
    ChatMessageForm,
    DeleteAccountForm,
    InviteToGameForm,
    PasswordChangeUserForm,
    PasswordResetUserForm,
    ProfileAvatarForm,
    SetPasswordUserForm,
    SocialForm,
    StoreItemActionForm,
    UserProfileForm,
    UpdateUserProfileForm,
    TwoFactorAuthSetupForm,
    JWTTokenForm,
    AuthenticationUserForm,
    TournamentForm,
)
from .models import (
    BlockedUser,
    ChatMessage,
    GameWarning,
    VerifyToken,
    UserProfile,
    Game,
    TwoFactorAuth,
    JWTToken,
    UserGameStat,
    Tournament,
    UserItem,
    StoreItem,
    OAuthToken,
    Room,
    Message,
)
from .utils import delete_from_media, get_equipped_item_value, pass2fa
from os import environ
from datetime import datetime, timedelta
from django.utils.http import urlsafe_base64_decode
import urllib.parse
import urllib.request
from urllib.parse import urlencode
import json
from django.core.files import File
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random


### Homepage and Error Page ###


@never_cache
def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "base.html")


@login_required()
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
            return HttpResponseRedirect("login")
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
    if request.user.is_authenticated and request.user.is_42student:
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
        # Create a context that doesn't verify SSL certificates
        # Create a SSL context
        # ssl_context = ssl.create_default_context()

        # Load your certificate
        # ssl_context.load_cert_chain(certfile='path/to/certfile', keyfile='path/to/keyfile')
        ssl_context = ssl._create_unverified_context()  # TODO temporary solution
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
        response = urllib.request.urlopen(
            req, context=ssl_context
        )  # TODO temporary solution

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
        user_info_response = urllib.request.urlopen(
            req, context=ssl_context
        )  # TODO temporary solution

        if user_info_response.status == 200:
            user_data = json.loads(user_info_response.read().decode("utf-8"))
            """with open('user_data.json', 'w') as file:
                json.dump(user_data, file) """

            if UserProfile.objects.filter(email=user_data["email"]).exists():
                user = UserProfile.objects.get(email=user_data["email"])
            else:
                user, created = UserProfile.objects.get_or_create(
                    username=user_data["login"]
                )
                if not created:
                    user = UserProfile.objects.create(
                        username=user_data["login"] + "42"
                    )
                else:
                    # Update user profile
                    user.set_unusable_password()
                    user.displayname = user_data.get("displayname", "")
                    user.email = user_data.get("email", "")
                    user.is_verified = True
                    user.is_42student = True
                    image_url = (
                        user_data.get("image", {}).get("versions", {}).get("medium", "")
                    )
                    if image_url:
                        image_name, response = urllib.request.urlretrieve(image_url)
                        file = File(open(image_name, "rb"))
                        user.avatar.save(f"{file.name}.jpg", file, save=False)
                        file.close()
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
        return HttpResponseRedirect("dashboard")
    if request.method == "POST":
        form = AuthenticationUserForm(request, request.POST)
        if form.is_valid():

            user = form.get_user()
            """  if not user.is_verified: #TODO confirm_login_allowed make this unnecessary?
                messages.error(request, "Account not verified")
                return redirect('login') """

            login(request, user)
            return HttpResponseRedirect("dashboard")
    else:
        form = AuthenticationUserForm()
    return render(
        request,
        "login.html",
        {"form": form},
    )


@never_cache
@login_required()
def logout_view(request):
    logout(request)
    return redirect("login")


### Profile ###

""" @login_required()
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user}) """


@never_cache
@login_required()
def profile_view(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    game_records = Game.objects.filter(
        Q(player1=profile) | Q(player2=profile)
    ).order_by("-created_at")
    paginator = Paginator(game_records, 5)  # Sayfada 5 kayıt göster
    page_number = request.GET.get("page")
    is_friend = request.user.friends.filter(id=profile.id).exists()
    if profile.elo_point is not None:
        profile.rank = UserProfile.objects.filter(
            elo_point__isnull=False,
            elo_point__gt=profile.elo_point,
        )   .exclude(
            username='IndianAI'  # Exclude user with the username 'IndianAI'
        ).order_by("-elo_point").count() + 1

    else:
        profile.rank = None

    try:
        history_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Sayfa numarası bir tamsayı değilse, ilk sayfayı al
        history_page_obj = paginator.page(1)
    except EmptyPage:
        # Geçersiz bir sayfa numarası istenirse, son sayfayı al
        history_page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "history_page_obj": history_page_obj,
            "is_friend": is_friend,
        },
    )


## Rps Game ##
@never_cache
@login_required()
def rps_game_find(request):
    return render(request, "rps-game-find.html")


## Pong Game ##
@never_cache
@login_required()
def pong_game_find(request):
    return render(request, "pong-game-find.html")

## Tournament Room List ##
@never_cache
@login_required()
def tournament_room_list(request):
    return render(request, "room-list.html")


### Profile Settings ###
@login_required()
def profile_settings(request, username):
    if request.user.username != username:
        return redirect(
            reverse("profile_settings", kwargs={"username": request.user.username})
        )
    profile = get_object_or_404(UserProfile, username=username)
    avatar_form = ProfileAvatarForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    profile_form = UpdateUserProfileForm(request.POST or None, instance=request.user)
    password_form = PasswordChangeUserForm(request.user, request.POST or None)
    social_form = SocialForm(request.POST or None, instance=request.user.social)
    delete_account_form = DeleteAccountForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if "avatar_form" in request.POST:
            if avatar_form.is_valid():
                # Delete old avatar file from MEDIA_ROOT
                if profile.avatar:
                    delete_from_media(profile.avatar.path)
                profile.avatar = avatar_form.cleaned_data["avatar"]
                profile.save()
                messages.success(request, "Avatar updated successfully.")
                return redirect(
                    reverse("profile_settings", args=[username]) + "#editProfile"
                )
        elif "profile_form" in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect(
                    reverse("profile_settings", args=[username]) + "#editProfile"
                )
        elif "password_form" in request.POST:
            if password_form.is_valid():
                profile.set_password(password_form.cleaned_data["new_password1"])
                profile.save()
                update_session_auth_hash(request, profile)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect(
                    reverse("profile_settings", args=[username]) + "#changePassword"
                )
        elif "social_form" in request.POST:
            if social_form.is_valid():
                social = social_form.save()
                profile.social = social
                profile.save()
                messages.success(request, "Socials updated successfully.")
                return redirect(
                    reverse("profile_settings", args=[username]) + "#addSocial"
                )
        elif "delete_account_form" in request.POST:
            if delete_account_form.is_valid():
                if profile.avatar:
                    delete_from_media(profile.avatar.path)
                profile.delete()
                return redirect("logout")
    else:
        avatar_form = ProfileAvatarForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user)
        password_form = PasswordChangeUserForm(request.user)
        social_form = SocialForm(instance=request.user.social)
        delete_account_form = DeleteAccountForm(user=request.user)

    return render(
        request,
        "profile-settings.html",
        {
            "profile": profile,
            "avatar_form": avatar_form,
            "profile_form": profile_form,
            "password_form": password_form,
            "social_form": social_form,
            "delete_account_form": delete_account_form,
        },
    )


@never_cache
@login_required()
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
@login_required()
def tournament(request):
    return render(request, "tournament.html")

@never_cache
@login_required()
def tournament_room(request):
    return render(request, "tournament-room.html")

@never_cache
@login_required()
def tournament_create(request):
    return render(request, "create-tournament.html")



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
@login_required()
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
@login_required()
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
@login_required()
def dashboard(request):
    profile = get_object_or_404(UserProfile, username=request.user.username)
    return render(request, "dashboard.html", {"profile": profile})


@never_cache
@login_required()
def rankings(request):
    top_users = UserProfile.objects.filter(
        game_stats__total_win_rate_pong__isnull=False
    ).exclude(username='IndianAI').order_by("-elo_point")[:3]

    # Her bir kullanıcıya sıra numarası eklemek için döngü
    for index, user in enumerate(top_users, start=1):
        user.rank = index
    
    other_users = UserProfile.objects.filter(
        game_stats__total_win_rate_pong__isnull=False
    ).exclude(username='IndianAI').order_by("-elo_point")[3:]

    for index, user in enumerate(other_users, start=4):
        user.rank = index

    paginator = Paginator(other_users, 3)
    page_number = request.GET.get("page")
    try:
        users_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        users_page_obj = paginator.page(1)
    except EmptyPage:
        users_page_obj = paginator.page(paginator.num_pages)

    # Add rank attribute to each user in the page

    return render(request, "rankings.html", {"top_users": top_users, "users_page_obj": users_page_obj})


@login_required()
def store(request, username):  # store_view
    if request.user.username != username:
        return redirect(reverse("store", kwargs={"username": request.user.username}))
    profile = get_object_or_404(UserProfile, username=username)
    bought_items = UserItem.objects.filter(user=profile, is_bought=True).values_list(
        "item", flat=True
    )
    store_items = StoreItem.objects.exclude(id__in=bought_items)
    if request.method == "POST":
        form = StoreItemActionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            action = form.cleaned_data["action"]
            whatis = form.cleaned_data["whatis"]
            if action == "buy":
                if UserItem.objects.filter(user=profile, item__name=name).exists():
                    messages.error(request, "Bu öğeyi zaten satın aldınız.")
                # Check if the user can afford the item, then create a new Purchase object
                else:
                    item = StoreItem.objects.get(name=name)
                    if item.price <= profile.indian_wallet:
                        profile.indian_wallet -= item.price
                        user_item = UserItem.objects.create(
                            user=profile, item=item, whatis=whatis, is_bought=True
                        )
                        profile.store_items.add(user_item.item)
                        profile.save()
                    else:
                        messages.error(
                            request,
                            "You don't have enough Indian Wallet to buy this item.",
                        )

    else:
        # category areas
        form = StoreItemActionForm()
        category_name = request.GET.get("category_name")
        if category_name and category_name != "All":
            store_items = store_items.filter(Q(category_name=category_name) | Q(category_name="All"))

    return render(
        request,
        "store.html",
        {"store_items": store_items, "profile": profile, "form": form},
    )


@never_cache
@login_required
def inventory(request, username):
    if request.user.username != username:
        return redirect(reverse("store", kwargs={"username": request.user.username}))
    profile = get_object_or_404(UserProfile, username=username)
    inventory_items = UserItem.objects.filter(user=profile).all()

    if request.method == "POST":
        form = StoreItemActionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            action = form.cleaned_data["action"]
            whatis = form.cleaned_data["whatis"]
            if action == "equip":
                # Check if the user has the item
                user_item = UserItem.objects.filter(
                    user=profile, item__name=name
                ).first()
                # Set the user's item to equipped
                if user_item:
                    user_item.is_equipped ^= True
                    user_item.save()
            elif action == "customize":
                # Check if the user has the item
                user_item = UserItem.objects.filter(
                    user=profile, item__name=name
                ).first()
                # Change user's equipped_item with the given name
                if user_item:
                    user_item.whatis = whatis
                    user_item.save()
    else:
        # category areas
        form = StoreItemActionForm()
        category_name = request.GET.get("category_name")

        if category_name and category_name != "All":
            inventory_items = UserItem.objects.filter(
                Q(item__category_name=category_name) | Q(item__category_name="All"),
                user=profile
            )
    return render(
        request,
        "inventory.html",
        {"profile": profile, "inventory_items": inventory_items}
    )

@login_required()
def search(request):
    if request.method == "POST":
        search_query = request.POST.get("search_query", "")
        request.session["search_query"] = search_query
    else:
        search_query = request.session.get("search_query", "")

    if search_query:
        search_query_email = search_query.split("@")[0]
        results = UserProfile.objects.filter(
            Q(username__icontains=search_query)
            | Q(displayname__icontains=search_query)
            | Q(email__icontains=search_query_email)
        ).exclude(username=request.user)
        results_list = []
        for result in results:
            # Create a dictionary with the data of the result
            result_dict = model_to_dict(result)
            # Add 'is_friend' key to the dictionary
            result_dict["is_friend"] = request.user.friends.filter(
                id=result.id
            ).exists()
            # Add social media information to the dictionary
            if result.social:
                result_dict["social"] = model_to_dict(result.social)
            if result.game_stats:
                result_dict["game_stats"] = model_to_dict(result.game_stats)
            # Append the dictionary to the list
            results_list.append(result_dict)
        paginator = Paginator(results_list, 8)
        page_number = request.GET.get("page")
        try:
            results = paginator.page(page_number)
        except PageNotAnInteger:
            # If page number is not an integer, deliver the first page
            results = paginator.page(1)
        except EmptyPage:
            # If page number is out of range, deliver the last page
            results = paginator.page(paginator.num_pages)
        return render(request, "search.html", {"results": results})
    return render(request, "search.html")



@login_required()
def friends(request, profile):
    profile = get_object_or_404(UserProfile, username=profile)
    friends = profile.friends.all().exclude(username=profile)
    friends = Paginator(friends, 8)
    page_number = request.GET.get("page")
    try:
        friends = friends.page(page_number)
    except PageNotAnInteger:
        # Sayfa numarası bir tamsayı değilse, ilk sayfayı al
        friends = friends.page(1)
    except EmptyPage:
        # Geçersiz bir sayfa numarası istenirse, son sayfayı al
        friends = friends.page(friends.num_pages)
    return render(request, "friends.html", {"friends": friends, "profile": profile})


@login_required()
def follow_unfollow(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    data = json.loads(request.body)
    action = data.get("action", "")
    if action == "follow":
        request.user.friends.add(profile)
    elif action == "unfollow":
        request.user.friends.remove(profile)
    else:
        return JsonResponse({"status": "error", "message": "Invalid action"})
    return JsonResponse({"status": "ok"})


@login_required()
def game(request):
    return render(request, "game.html")


@login_required()
def play_ai(request):
    user_items = UserItem.objects.filter(user=request.user)
    
    # Just Customizations - PONG
    ainametag = get_equipped_item_value(user_items, "My Beautiful AI", "IndianAI")
    paddlecolor = get_equipped_item_value(user_items, "My Beautiful Paddle", "black")
    playgroundcolor = get_equipped_item_value(user_items, "My Playground", "lightgrey")
    
    
    # Just Abilities - PONG
    giantman = get_equipped_item_value(user_items, "Giant-Man", "None")
    likeacheater = get_equipped_item_value(user_items, "Like a Cheater", "None")
    fastandfurious = get_equipped_item_value(user_items, "Fast and Furious", "None")
    rageoffire = get_equipped_item_value(user_items, "Rage of Fire", "None")
    frozenball = get_equipped_item_value(user_items, "Frozen Ball", "None")
    givemethemusic = get_equipped_item_value(user_items, "DJ Give Me The Music", "None")

    return render(request, "play-ai.html", {"ainametag": ainametag, "paddlecolor": paddlecolor, "playgroundcolor": playgroundcolor, "giantman": giantman, "likeacheater": likeacheater, "fastandfurious": fastandfurious, "rageoffire": rageoffire, "frozenball": frozenball, "givemethemusic": givemethemusic})

@never_cache
@login_required()
def local_game(request):
    user_items = UserItem.objects.filter(user=request.user)
    
    # Just Customizations - PONG
    player2name = "Player 2"
    paddlecolor = get_equipped_item_value(user_items, "My Beautiful Paddle", "black")
    playgroundcolor = get_equipped_item_value(user_items, "My Playground", "lightgrey")
    
    # Just Abilities - PONG
    giantman = get_equipped_item_value(user_items, "Giant-Man", "None")
    likeacheater = get_equipped_item_value(user_items, "Like a Cheater", "None")
    fastandfurious = get_equipped_item_value(user_items, "Fast and Furious", "None")
    rageoffire = get_equipped_item_value(user_items, "Rage of Fire", "None")
    frozenball = get_equipped_item_value(user_items, "Frozen Ball", "None")
    return render(request, "local-game.html", {"player2name": player2name, "paddlecolor": paddlecolor, "playgroundcolor": playgroundcolor, "giantman": giantman, "likeacheater": likeacheater, "fastandfurious": fastandfurious, "rageoffire": rageoffire, "frozenball": frozenball})


@never_cache
@login_required()
def chat(request):
    users = UserProfile.objects.all().exclude(username=request.user)
    return render(request, "chat.html", {"users": users})


@login_required()
def aboutus(request):
    return render(request, "aboutus.html")


@login_required()
def match_history(request, profile):
    profile = get_object_or_404(UserProfile, username=profile)
    
    return render(request, "match-history.html", {"profile": profile})


### New Chat ###
@login_required()
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


@login_required()
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
@login_required()
def chat_room(request):
    messages_sent = ChatMessage.objects.filter(sender=request.user)
    messages_received = ChatMessage.objects.filter(receiver=request.user)
    context = {"messages_sent": messages_sent, "messages_received": messages_received}
    return render(request, "chat_room.html", context)


@never_cache
@login_required()
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
@login_required()
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
@login_required()
def unblock_user(request, blocked_user_id):
    blocked_user = UserProfile.objects.get(id=blocked_user_id)
    BlockedUser.objects.filter(user=request.user, blocked_user=blocked_user).delete()
    messages.success(request, f"You have unblocked {blocked_user.username}.")
    return redirect("chat")


@never_cache
@login_required()
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
@login_required()
def game_warning(request, opponent_id):
    opponent = UserProfile.objects.get(id=opponent_id)
    GameWarning.objects.create(user=request.user, opponent=opponent)
    messages.warning(request, f"Game warning sent to {opponent.username}.")
    return redirect("chat")


### Tournaments ###


@never_cache
@login_required()
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


""" @never_cache
@login_required()
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
    return render(request, "create_tournament_match.html", {"form": form}) """


### Two-Factor Authentication ###


@never_cache
@login_required()
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
@login_required()
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


# Game logics #


@csrf_exempt
def update_winner(request):
    if request.method == "POST":
        data = json.loads(request.body)
        winner = data.get("winner")
        loser = data.get("loser")
        winnerscore = data.get("winnerscore")
        loserscore = data.get("loserscore")
        start_time = data.get("start_time")
        finish_time = data.get("finish_time")

        winner_profile = get_object_or_404(UserProfile, username=winner)
        loser_profile = get_object_or_404(UserProfile, username=loser)

        if winner:
            winner_profile.indian_wallet += random.randint(300, 500)
            winner_profile.elo_point += random.randint(20, 30)
            winner_profile.save()
        elif loser:
            loser_profile.indian_wallet += random.randint(20, 30)
            lose_elo -= random.randint(10, 20)
            if lose_elo < loser_profile.elo_point:
                loser_profile.elo_point -= lose_elo
            loser_profile.save()

        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        finish_time = datetime.strptime(finish_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        game_duration = finish_time - start_time

        game_record = Game.objects.create(
            group_name=winner_profile.username + "_" + loser_profile.username,
            player1=winner_profile,
            player2=loser_profile,
            player1_score=winnerscore,
            player2_score=loserscore,
            winner=winner_profile,
            loser=loser_profile,
            game_duration=game_duration,
        )

        if winner_profile.game_stats is None:
            winner_profile.game_stats = UserGameStat.objects.create()
            winner_profile.save()
        if loser_profile.game_stats is None:
            loser_profile.game_stats = UserGameStat.objects.create()
            loser_profile.save()
        # Game Stats #

        # Winner #
        winner_profile.game_stats.total_games_pong += 1

        winner_profile.game_stats.total_win_pong += 1
        winner_profile.game_stats.total_win_rate_pong = (
            winner_profile.game_stats.total_win_pong
            / winner_profile.game_stats.total_games_pong
        )
        winner_profile.game_stats.total_win_streak_pong += 1
        winner_profile.game_stats.total_lose_streak_pong = 0

        # Kazananın ortalama puan kazanma ve kaybetme sayılarını güncelle
        winner_profile.game_stats.total_avg_points_won_pong = (
            winner_profile.game_stats.total_avg_points_won_pong
            * (winner_profile.game_stats.total_win_pong - 1)
            + winnerscore
        ) / winner_profile.game_stats.total_win_pong
        winner_profile.game_stats.total_avg_points_lost_pong = (
            winner_profile.game_stats.total_avg_points_lost_pong
            * (winner_profile.game_stats.total_win_pong - 1)
            + loserscore
        ) / winner_profile.game_stats.total_win_pong
        total_game_duration_seconds = (
            winner_profile.game_stats.total_avg_game_duration_pong.total_seconds()
            * (winner_profile.game_stats.total_games_pong - 1)
        )
        total_game_duration_seconds += game_duration.total_seconds()
        avg_game_duration_seconds = (
            total_game_duration_seconds / winner_profile.game_stats.total_games_pong
        )
        winner_profile.game_stats.total_avg_game_duration_pong = timedelta(
            seconds=avg_game_duration_seconds
        )
        winner_profile.game_stats.save()

        # Loser #
        loser_profile.game_stats.total_games_pong += 1

        loser_profile.game_stats.total_lose_pong += 1
        loser_profile.game_stats.total_win_rate_pong = (
            loser_profile.game_stats.total_win_pong
            / loser_profile.game_stats.total_games_pong
        )
        loser_profile.game_stats.total_win_streak_pong = 0
        loser_profile.game_stats.total_lose_streak_pong += 1

        # Kaybedenin ortalama puan kazanma ve kaybetme sayılarını güncelle
        loser_profile.game_stats.total_avg_points_won_pong = (
            loser_profile.game_stats.total_avg_points_won_pong
            * (loser_profile.game_stats.total_lose_pong - 1)
            + loserscore
        ) / loser_profile.game_stats.total_lose_pong
        loser_profile.game_stats.total_avg_points_lost_pong = (
            loser_profile.game_stats.total_avg_points_lost_pong
            * (loser_profile.game_stats.total_lose_pong - 1)
            + winnerscore
        ) / loser_profile.game_stats.total_lose_pong
        loser_total_game_duration_seconds = (
            loser_profile.game_stats.total_avg_game_duration_pong.total_seconds()
            * (loser_profile.game_stats.total_games_pong - 1)
        )
        loser_total_game_duration_seconds += game_duration.total_seconds()
        loser_avg_game_duration_seconds = (
            loser_total_game_duration_seconds
            / loser_profile.game_stats.total_games_pong
        )
        loser_profile.game_stats.total_avg_game_duration_pong = timedelta(
            seconds=loser_avg_game_duration_seconds
        )
        loser_profile.game_stats.save()

        ##############
        return JsonResponse({"message": "Winner and Loser updated successfully"})
    return render(request, "404.html", status=404)
