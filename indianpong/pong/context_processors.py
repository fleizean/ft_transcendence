from django.shortcuts import get_object_or_404
from .models import UserProfile

def userinfo(request):
    if not request.user.is_authenticated:
        return {}
    """     excluded_paths = ['/login']      #TODO Maybe this is not required
    if request.path in excluded_paths:
        return {}
     """
    profile = get_object_or_404(UserProfile, username=request.user.username)
    #profile_avatar = profile.avatar.url if profile.avatar else "/static/assets/profile/profilephoto.jpeg"
    return {'username': profile.username, 'avatar': profile.avatar.url, 'is_online': profile.is_online, 'is_playing': profile.is_playing}