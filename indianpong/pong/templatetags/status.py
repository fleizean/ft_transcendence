from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def is_user_online(user_id):
    return cache.get(f'online_{user_id}', default=False)

@register.simple_tag
def is_user_playing(user_id):
    return cache.get(f'playing_{user_id}', default=False)