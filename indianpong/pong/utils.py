import base64, hashlib, os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from asgiref.sync import sync_to_async
import threading

def pass2fa(request, user_obj):
	if user_obj.has_2fa:
		hashed_secret = hashlib.sha512((user_obj.username + os.environ.get("OTP_SECRET")).encode("utf-8")).digest()
		encoded_secret = base64.b32encode(hashed_secret)
		return render(request, "pass2fa.html", {"user": user_obj.username,"key": encoded_secret})
	else:
		login(request, user_obj)
		return redirect("index")
	
class ThreadSafeDict:
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    @sync_to_async
    def get(self, key, default=None):
        with self.lock:
            return self.dict.get(key, default)

    @sync_to_async
    def set(self, key, value):
        with self.lock:
            self.dict[key] = value

    @sync_to_async
    def delete(self, key):
        with self.lock:
            if key in self.dict:
                del self.dict[key]

    @sync_to_async
    def get_keys_with_value(self, value):
        with self.lock:
            return [k for k, v in self.dict.items() if v == value]