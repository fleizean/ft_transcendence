from django.core.management.base import BaseCommand
from pong.models import UserProfile, StoreItem
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not UserProfile.objects.filter(username="IndianAI").exists():
           user = UserProfile.objects.create_user(username="IndianAI", email="indianpong@gmail.com")
           user.set_unusable_password()
           user.displayname = "Sitting AI"
           user.avatar = "indianai_207d5c7.jpg"
           user.is_verified = True
           user.indian_wallet = 1000
           user.elo_point = 1000
           user.save()
        with open('store_data.json') as f:
            data = json.load(f)

        for item_data in data:
            StoreItem.objects.create(**item_data)

        self.stdout.write(self.style.SUCCESS('Store data loaded successfully.'))
  