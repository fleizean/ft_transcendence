from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def is_user_online(user_username):
    return cache.get(f'online_{user_username}', default=False)

@register.simple_tag
def is_user_playing(user_username):
    return cache.get(f'playing_{user_username}', default=False)