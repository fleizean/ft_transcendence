from django.core.management.base import BaseCommand
from pong.models import UserProfile

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