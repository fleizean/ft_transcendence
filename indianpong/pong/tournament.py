import random

class Tournament:
    def __init__(self, participants):
        self.participants = participants

    def create_matches(self):
        matches = []
        random.shuffle(self.participants)
        while len(self.participants) > 1:
            match = (self.participants.pop(), self.participants.pop())
            matches.append(match)
        return matches

    def run_tournament(self):
        winners = self.participants.copy()
        while len(winners) > 1:
            next_round = []
            for i in range(0, len(winners), 2):
                match_winner = self.play_match(winners[i], winners[i+1])
                next_round.append(match_winner)
            winners = next_round.copy()
        return winners[0]

    def play_match(self, contender1, contender2):
        # Simulate a match between contender1 and contender2
        # Return the winner of the match
        # You can implement your own logic here
        # For example, you can randomly choose a winner
        return random.choice([contender1, contender2])
