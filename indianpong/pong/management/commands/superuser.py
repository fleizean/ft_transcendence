from django.core.management.base import BaseCommand
from pong.models import UserProfile
from os import environ

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not UserProfile.objects.filter(username="Bitlis").exists():
            UserProfile.objects.create_superuser("Bitlis", "bit@g.com", environ.get("SUPER_PASS", default="9247"))