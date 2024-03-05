from django.contrib.auth.hashers import make_password
from pong.models import UserProfile, UserGameStat, Social
from random import randint, choice
from django.core.management.base import BaseCommand
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        num_users = options['num_users']
        user_game_stats = []
        socials = []
        user_profiles = []
        password = make_password('123456a.')

        for i in range(num_users):
            username = "Indian" + str(i)
            displayname = "Original Indian" + str(i)
            email = username + '@indian.com'

            # Prepare UserGameStat instance
            game_stat = UserGameStat(
                total_games_pong=randint(0, 100),
                total_win_pong=randint(0, 100),
                total_lose_pong=randint(0, 100),
                total_win_streak_pong=randint(0, 100),
                total_lose_streak_pong=randint(0, 100),
                total_win_rate_pong=randint(0, 100) / 100.0,
                total_avg_game_duration_pong=timedelta(seconds=randint(0, 3600)),
                total_avg_points_won_pong=randint(0, 100),
                total_avg_points_lost_pong=randint(0, 100)
            )
            user_game_stats.append(game_stat)

            # Prepare Social instance
            social = Social(
                intra42 = username,
                linkedin = username,
                github = username,
                twitter= username,
            )
            socials.append(social)

            # Prepare UserProfile instance
            user_profile = UserProfile(
                username=username, 
                email=email, 
                displayname=displayname, 
                password=password, 
                game_stats=game_stat,
                social=social
            )
            user_profiles.append(user_profile)

        # Create instances in database
        UserGameStat.objects.bulk_create(user_game_stats)
        Social.objects.bulk_create(socials)
        #UserProfile.objects.bulk_create(user_profiles)
        # Create UserProfile instances individually to trigger save method
        for user_profile in user_profiles:
            user_profile.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_users} users.'))