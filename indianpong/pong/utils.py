import base64, hashlib, os
from django.shortcuts import render, redirect
from django.contrib.auth import login
import asyncio

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
