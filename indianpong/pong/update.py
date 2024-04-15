
from datetime import timedelta
import random

def update_tournament(game):
    from .models import Tournament

    tournament = Tournament.objects.get(id=game.tournament_id)
    tournament.played_games_count += 1
    if tournament.played_games_count == 2:
        tournament.create_final_round_matches()
    elif tournament.played_games_count == 3:
        tournament.status = "ended"
        tournament.winner = game.winner
    #? Maybe save end_date
    tournament.save()


def update_wallet_elo(winner, loser):
    winner.indian_wallet += random.randint(300, 500)
    winner.elo_point += random.randint(20, 30)

    loser.indian_wallet += random.randint(20, 30)
    lose_elo = random.randint(10, 20)
    if lose_elo < loser.elo_point:
        loser.elo_point -= lose_elo
    winner.save()
    loser.save()


def update_stats_pong(winner, loser, winnerscore, loserscore, game_duration, game_type):
    # Update total games count
    winner.game_stats_pong.total_games_pong += 1
    loser.game_stats_pong.total_games_pong += 1
    

    # Update stats for winner
    winner.game_stats_pong.total_win_pong += 1
    winner.game_stats_pong.total_win_streak_pong += 1
    winner.game_stats_pong.total_lose_streak_pong = 0
    
    # Update average points won and lost for winner
    winner.game_stats_pong.total_avg_points_won_pong = ((winner.game_stats_pong.total_avg_points_won_pong * (winner.game_stats_pong.total_win_pong - 1)) + winnerscore) / winner.game_stats_pong.total_win_pong
    winner.game_stats_pong.total_avg_points_lost_pong = ((winner.game_stats_pong.total_avg_points_lost_pong * (winner.game_stats_pong.total_win_pong - 1)) + loserscore) / winner.game_stats_pong.total_win_pong
        
    # Update stats for loser
    loser.game_stats_pong.total_lose_pong += 1
    loser.game_stats_pong.total_win_rate_pong = (loser.game_stats_pong.total_win_pong / loser.game_stats_pong.total_games_pong)
    loser.game_stats_pong.total_win_streak_pong = 0
    loser.game_stats_pong.total_lose_streak_pong += 1
    
    # Update average points won and lost for loser
    loser.game_stats_pong.total_avg_points_won_pong = ((loser.game_stats_pong.total_avg_points_won_pong * (loser.game_stats_pong.total_lose_pong - 1)) + loserscore) / loser.game_stats_pong.total_lose_pong
    loser.game_stats_pong.total_avg_points_lost_pong = ((loser.game_stats_pong.total_avg_points_lost_pong * (loser.game_stats_pong.total_lose_pong - 1)) + winnerscore) / loser.game_stats_pong.total_lose_pong

    # Update total win rate
    winner.game_stats_pong.total_win_rate_pong = (winner.game_stats_pong.total_win_pong / winner.game_stats_pong.total_games_pong)
    loser.game_stats_pong.total_win_rate_pong = (loser.game_stats_pong.total_win_pong / loser.game_stats_pong.total_games_pong)
    
    # Update total average game duration for both winner and loser
    winner_total_game_duration_seconds = winner.game_stats_pong.total_avg_game_duration_pong.total_seconds() * (winner.game_stats_pong.total_games_pong - 1)
    loser_total_game_duration_seconds = loser.game_stats_pong.total_avg_game_duration_pong.total_seconds() * (loser.game_stats_pong.total_games_pong - 1)

    if game_type != "not_remote":
        winner_total_game_duration_seconds += game_duration
        loser_total_game_duration_seconds += game_duration
    else:
        winner_total_game_duration_seconds += game_duration.total_seconds()
        loser_total_game_duration_seconds += game_duration.total_seconds()
    
    winner_avg_game_duration_seconds = winner_total_game_duration_seconds / winner.game_stats_pong.total_games_pong
    winner.game_stats_pong.total_avg_game_duration_pong = timedelta(seconds=winner_avg_game_duration_seconds)
    loser_avg_game_duration_seconds = loser_total_game_duration_seconds / loser.game_stats_pong.total_games_pong
    loser.game_stats_pong.total_avg_game_duration_pong = timedelta(seconds=loser_avg_game_duration_seconds)

    # Save updated stats
    winner.game_stats_pong.save()
    loser.game_stats_pong.save()


def update_stats_rps(winner, loser, winnerscore, loserscore, game_duration, game_type):
    # Update total games count
    winner.game_stats_rps.total_games_rps += 1
    loser.game_stats_rps.total_games_rps += 1
    
    # Update stats for winner
    winner.game_stats_rps.total_win_rps += 1
    winner.game_stats_rps.total_win_streak_rps += 1
    winner.game_stats_rps.total_lose_streak_rps = 0
    
    # Update average points won and lost for winner
    winner.game_stats_rps.total_avg_points_won_rps = ((winner.game_stats_rps.total_avg_points_won_rps * (winner.game_stats_rps.total_win_rps - 1)) + winnerscore) / winner.game_stats_rps.total_win_rps
    winner.game_stats_rps.total_avg_points_lost_rps = ((winner.game_stats_rps.total_avg_points_lost_rps * (winner.game_stats_rps.total_win_rps - 1)) + loserscore) / winner.game_stats_rps.total_win_rps
        

    # Update stats for loser
    loser.game_stats_rps.total_lose_rps += 1
    loser.game_stats_rps.total_win_rate_rps = (loser.game_stats_rps.total_win_rps / loser.game_stats_rps.total_games_rps)
    loser.game_stats_rps.total_win_streak_rps = 0
    loser.game_stats_rps.total_lose_streak_rps += 1
    
    # Update average points won and lost for loser
    loser.game_stats_rps.total_avg_points_won_rps = ((loser.game_stats_rps.total_avg_points_won_rps * (loser.game_stats_rps.total_lose_rps - 1)) + loserscore) / loser.game_stats_rps.total_lose_rps
    loser.game_stats_rps.total_avg_points_lost_rps = ((loser.game_stats_rps.total_avg_points_lost_rps * (loser.game_stats_rps.total_lose_rps - 1)) + winnerscore) / loser.game_stats_rps.total_lose_rps
    
    # Update total win rate
    winner.game_stats_rps.total_win_rate_rps = (winner.game_stats_rps.total_win_rps / winner.game_stats_rps.total_games_rps)
    loser.game_stats_rps.total_win_rate_rps = (loser.game_stats_rps.total_win_rps / loser.game_stats_rps.total_games_rps)
    
    winner_total_game_duration_seconds = winner.game_stats_rps.total_avg_game_duration_rps.total_seconds() * (winner.game_stats_rps.total_games_rps - 1)
    loser_total_game_duration_seconds = loser.game_stats_rps.total_avg_game_duration_rps.total_seconds() * (loser.game_stats_rps.total_games_rps - 1)
    # Update total average game duration for winner
    if game_type != "not_remote":
        winner_total_game_duration_seconds += game_duration
        loser_total_game_duration_seconds += game_duration
    else:
        winner_total_game_duration_seconds += game_duration.total_seconds()
        loser_total_game_duration_seconds += game_duration.total_seconds()
        
        
    winner_avg_game_duration_seconds = winner_total_game_duration_seconds / winner.game_stats_rps.total_games_rps
    winner.game_stats_rps.total_avg_game_duration_rps = timedelta(seconds=winner_avg_game_duration_seconds)
    loser_avg_game_duration_seconds = loser_total_game_duration_seconds / loser.game_stats_rps.total_games_rps
    loser.game_stats_rps.total_avg_game_duration_rps = timedelta(seconds=loser_avg_game_duration_seconds)
    
    # Save updated stats
    winner.game_stats_rps.save()
    loser.game_stats_rps.save()