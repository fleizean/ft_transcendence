from django import template
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from pong.models import UserProfile

register = template.Library()

@register.simple_tag(takes_context=True)
def user_info(context):
    request = context['request']

    profile = get_object_or_404(UserProfile, username=request.user.username)
    is_online = cache.get(f'online_{profile.username}', default=False)
    is_playing = cache.get(f'playing_{profile.username}', default=False)
    return {'username': profile.username, 'avatar': profile.avatar.url, 'is_online': is_online, 'is_playing': is_playing}