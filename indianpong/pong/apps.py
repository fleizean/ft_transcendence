from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class PongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pong'

    def ready(self):
        from .models import UserProfile  # Buraya taşıdık
        User = get_user_model()

        @receiver(user_logged_in, sender=User)
        def user_logged_in_handler(sender, request, user, **kwargs):
            profile = UserProfile.objects.get(displayname=user.displayname)
            profile.is_online = True
            profile.is_offline = False
            profile.save()

        @receiver(user_logged_out, sender=User)
        def user_logged_out_handler(sender, request, user, **kwargs):
            try:
                profile = UserProfile.objects.get(displayname=user.displayname)
                profile.is_online = False
                profile.is_offline = True
                profile.save()
            except UserProfile.DoesNotExist:
                pass

