"""
URL configuration for indianpong project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from pong.views import aboutus, update_winner, inventory, store, activate_account, play_ai, pong_game_find, rps_game_find, auth_callback, chat, friends, match_history, password_change, password_reset, password_reset_done, rankings, dashboard, game, index, auth, chat_room, profile_view, search, set_password, signup, login_view, logout_view, profile_settings, setup_two_factor_auth, generate_jwt_token, create_tournament, create_tournament_match, start_chat, room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('activate/<str:token>/', activate_account, name='activate'),
    path('login', login_view, name='login'),
    path('auth', auth, name='auth'),
    path('auth_callback', auth_callback, name='auth_callback'),
    path('logout', logout_view, name='logout'),
    path('rps-game-find', rps_game_find, name='rps_game_find'),
    path('pong-game-find', pong_game_find, name='pong_game_find'),
    path('play-ai', play_ai, name='play_ai'),
    path('chat', chat, name='chat'),
    path("start_chat/<str:username>", start_chat, name="start_chat"),
    path("chat/<str:room_name>/", room, name="room"),
    #path('chat_room', chat_room, name='chat_room'),
    path('dashboard', dashboard, name='dashboard'),
    path('friends/<str:profile>', friends, name='friends'),
    path('match-history/<str:profile>', match_history, name='match_history'),
    path('about-us', aboutus, name='aboutus'),
    path('rankings', rankings, name='rankings'),
    path('inventory/<str:username>/', inventory, name='inventory'),
    path('store/<str:username>/', store, name='store'),
    path('search', search, name='search'),
    path('pong-game', game, name='game'),
    path('update_winner', update_winner, name='update_winner'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('profile/<str:username>/settings', profile_settings, name='profile_settings'),
    path('password_change', password_change, name='password_change'),
    path('password_reset', password_reset, name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', password_reset, name='password_reset_confirm'),
    path('password_reset_done', password_reset_done, name='password_reset_done'),
    path('set_password/<str:uidb64>/<str:token>/', set_password, name='set_password'),
    path('setup_two_factor_auth', setup_two_factor_auth, name='setup_two_factor_auth'),
    path('generate_jwt_token', generate_jwt_token, name='generate_jwt_token'),
    path('create_tournament', create_tournament, name='create_tournament'),
    path('create_tournament_match', create_tournament_match, name='create_tournament_match'),
]

handler404 = 'pong.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)