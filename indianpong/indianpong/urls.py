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
from pong.views import auth_callback, chat, rankings, dashboard, game, index, auth, chat_room, profile_view, search, signup, login_view, logout_view, update_profile, setup_two_factor_auth, generate_jwt_token, create_tournament, create_tournament_match, start_chat, room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('login', login_view, name='login'),
    path('auth', auth, name='auth'),
    path('auth_callback', auth_callback, name='auth_callback'),
    path('logout', logout_view, name='logout'),
    
    #path('chat', chat, name='chat'),
    path("start_chat/<str:username>", start_chat, name="start_chat"),
    path("chat/<str:room_name>/", room, name="room"),
    #path('chat_room', chat_room, name='chat_room'),

    path('dashboard', dashboard, name='dashboard'),
    path('rankings', rankings, name='rankings'),
    path('search', search, name='search'),
    path('game', game, name='game'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('update_profile', update_profile, name='update_profile'),
    path('setup_two_factor_auth', setup_two_factor_auth, name='setup_two_factor_auth'),
    path('generate_jwt_token', generate_jwt_token, name='generate_jwt_token'),
    path('create_tournament', create_tournament, name='create_tournament'),
    path('create_tournament_match', create_tournament_match, name='create_tournament_match'),
]

handler404 = 'pong.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)