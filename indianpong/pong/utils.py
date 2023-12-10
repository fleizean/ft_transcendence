import base64, hashlib, os
from django.shortcuts import render, redirect
from django.contrib.auth import login

def pass2fa(request, user_obj):
	if user_obj.has_2fa:
		hashed_secret = hashlib.sha512((user_obj.username + os.environ.get("OTP_SECRET")).encode("utf-8")).digest()
		encoded_secret = base64.b32encode(hashed_secret)
		return render(request, "pass2fa.html", {"user": user_obj.username,"key": encoded_secret})
	else:
		login(request, user_obj)
		return redirect("index")