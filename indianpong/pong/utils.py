from django.shortcuts import render, redirect
from django.contrib.auth import login
import asyncio
import os
from django.utils.crypto import get_random_string
from django.core.files.base import ContentFile
import base64, hashlib
from django.core.cache import cache

def delete_from_media(path):
    if os.path.isfile(path):
        os.remove(path)

def get_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.username, get_random_string(length=7), ext)
    return filename


def create_random_svg(username):
    hash = hashlib.md5(username.encode()).hexdigest()
    hue = int(hash, 16) % 360
    svg_parts = []
    for i in range(25 if username else 0):
        if int(hash, 16) & (1 << (i % 15)):
            x = 7 - i // 5 if i > 14 else i // 5
            svg_parts.append(f'<rect x="{x}" y="{i % 5}" width="1" height="1"/>')
    svg_content = f'''
    <svg viewBox="-1.5 -1.5 8 8" xmlns="http://www.w3.org/2000/svg" fill="hsl({hue}, 95%, 45%)">
    {''.join(svg_parts)}
    </svg>
    '''
    return ContentFile(svg_content.encode('utf-8'))

def get_equipped_item_value(user_items, item_name, default_item):
    if (item_name == "My Playground" or item_name == "My Beautiful Paddle" or item_name == "My Beautiful AI"):
        item = user_items.filter(item__name=item_name, is_equipped=True).first()
        return item.whatis if item else default_item
    else:
        item = user_items.filter(item__name=item_name, is_equipped=True).first()
        return "true" if item else "false"

def pass2fa(request, user_obj):
	if user_obj.has_2fa:
		hashed_secret = hashlib.sha512((user_obj.username + os.environ.get("OTP_SECRET")).encode("utf-8")).digest()
		encoded_secret = base64.b32encode(hashed_secret)
		return render(request, "pass2fa.html", {"user": user_obj.username,"key": encoded_secret})
	else:
		login(request, user_obj)
		return redirect("index")
     
# This is a race-safe dictionary that can be used to store online status of users
# It is used to check if a user is online before inviting them to a game
# It is also used to get a list of online users to send to the client
# if you use redis-cache you can use it instead of this, redis already recommended for channels
# from django.core.cache import cache
# user_status = cache.get('user_status', {})
# user_status['username'] = 'online'
# cache.set('user_status', user_status)
# online_users = [k for k, v in user_status.items() if v == 'online']     
	
class AsyncLockedDict:
    def __init__(self):
        self.dict = {}
        self.lock = asyncio.Lock()

    async def get(self, key, default=None):
        async with self.lock:
            return self.dict.get(key, default)

    async def set(self, key, value):
        async with self.lock:
            self.dict[key] = value

    async def delete(self, key):
        async with self.lock:
            if key in self.dict:
                del self.dict[key]

    async def get_keys_with_value(self, value):
        async with self.lock:
            return [k for k, v in self.dict.items() if v == value]
        
    async def set_field_value(self, key, value, field_name):
        async with self.lock:
            setattr(self.dict[key], field_name, value)


def add_to_cache(key, container, value):
    container_ = cache.get(key, container)
    container_.add(value)
    cache.set(key, container_)

def remove_from_cache(key, container, value):
    container_ = cache.get(key, container)
    if container_:
        container_.remove(value)
        cache.set(key, container_)
