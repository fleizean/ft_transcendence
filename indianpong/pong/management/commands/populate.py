from django.core.management.base import BaseCommand
from pong.models import UserProfile
import random
import string

class Command(BaseCommand):
    help = 'Populates the database with users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        num_users = options['num_users']
        for i in range(num_users):
            username = "Indian" + str(i)
            displayname = "Original Indian" + str(i)
            email = username + '@indian.com'
            password = '123456a.'  # Replace with your desired password

            UserProfile.objects.create_user(username=username, email=email, displayname=displayname, password=password)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_users} users.'))
