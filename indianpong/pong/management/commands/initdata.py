from django.core.management.base import BaseCommand
from pong.models import UserProfile, StoreItem, Social
from django.core.files import File
from os import environ
import json

class Command(BaseCommand):
	def handle(self, *args, **options):
		# Create superuser if not exists
		superuser = environ.get("SUPER_USER", default="Bitlis")
		supermail = environ.get("SUPER_MAIL", default="bit@g.com")
		superpass = environ.get("SUPER_PASS", default="9247")
		if not UserProfile.objects.filter(username=superuser).exists():
			super_user = UserProfile.objects.create_superuser(superuser, supermail, superpass)
			file = File(open('static/assets/profile/default_avatar.jpeg', "rb"))
			super_user.avatar.save(f"{file.name}.jpg", file, save=False)
			file.close()
			super_user.indian_wallet = 1000
			super_user.save()
			self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
		# Create IndianAI if not exists
		if not UserProfile.objects.filter(username="IndianAI").exists():
			user = UserProfile.objects.create_user(username="IndianAI", email="indianpong@gmail.com")
			user.set_unusable_password()
			user.displayname = "Sitting AI"
			file = File(open('static/assets/profile/indianai.jpg', "rb"))
			user.avatar.save(f"{file.name}.jpg", file, save=False)
			file.close()
			user.is_verified = True
			user.is_online = True
			user.indian_wallet = 1000
			user.is_indianai = True
			user.elo_point = 1000
			user.save()
			self.stdout.write(self.style.SUCCESS('IndianAI created successfully.'))  
		# Load store data    
		with open('static/assets/stores/store_data.json') as f:
			data = json.load(f)

		for item_data in data:
			StoreItem.objects.create(**item_data)

		self.stdout.write(self.style.SUCCESS('Store data loaded successfully.'))


