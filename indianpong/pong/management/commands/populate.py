from django.core.management.base import BaseCommand
from pong.models import UserProfile
import random
import string

class Command(BaseCommand):
    help = 'Populates the database with 10 users'
    usernames = [
            "Indian1", "Indian2", "Indian3", "Indian4", "Indian5",
            "Indian6", "Indian7", "Indian8", "Indian9", "Indian10"
        ]
    displaynames = [
            "Original Indian 1", "Original Indian 2", "Original Indian 3", "Original Indian 4", "Original Indian 5",
            "Original Indian 6", "Original Indian 7", "Original Indian 8", "Original Indian 9", "Original Indian 10"
        ]
    def handle(self, *args, **options):
        for i in range(10):
            username = self.usernames[i]
            displayname = self.displaynames[i]
            email = username + '@indian.com'
            password = '123456a.'  # Replace with your desired password

            UserProfile.objects.create_user(username=username, email=email, displayname=displayname, password=password)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 10 users.'))