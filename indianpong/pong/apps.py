from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


class PongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pong'

"""     def ready(self):

        @receiver(user_logged_in)
        def user_logged_in_handler(sender, request, **kwargs):
            request.user.is_online = True
            request.user.save()

        @receiver(user_logged_out)
        def user_logged_out_handler(sender, request, **kwargs):
            request.user.is_online = False
            request.user.save() """

