import random

class Match:
    def __init__(self, player1, player2):
        self.group_name = f"{player1}_{player2}"
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        #self.status = "playing"
class Tournament:
    def __init__(self, tournament_id):
        self.id = tournament_id
        self.standings = list()
        self.matches = list()

    def create_matches(self):
        random.shuffle(self.standings)
        # Empty matches list for next round
        self.matches = list()
        while len(self.standings) > 1:
            self.matches.append(Match(self.standings.pop(), self.standings.pop()))
        return self.matches

    def run_tournament(self):
        winners = self.standings.copy()
        while len(winners) > 1:
            next_round = []
            for i in range(0, len(winners), 2):
                match_winner = self.play_match(winners[i], winners[i+1])
                next_round.append(match_winner)
            winners = next_round.copy()
        return winners[0]

    def play_match(self, player1, player2):
        # Simulate a match between player1 and player2
        # Return the winner of the match
        # You can implement your own logic here
        # For example, you can randomly choose a winner
        return random.choice([player1, player2])
