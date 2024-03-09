from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import UserProfile

def userinfo(request):
    if request.user.is_anonymous:
        return {}
    """     excluded_paths = ['/login']      #TODO Maybe this is not required
    if request.path in excluded_paths:
        return {}
     """
    profile = get_object_or_404(UserProfile, username=request.user.username)
    is_online = cache.get(f'online_{profile.username}', default=False)
    is_playing = cache.get(f'playing_{profile.username}', default=False)
    #profile_avatar = profile.avatar.url if profile.avatar else "/static/assets/profile/profilephoto.jpeg"
    return {'username': profile.username, 'avatar': profile.avatar.url, 'is_online': is_online, 'is_playing': is_playing}