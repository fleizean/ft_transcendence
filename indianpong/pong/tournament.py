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


class Tournament2:
    def __init__(self, creator, tournament_id):
        self.id = tournament_id
        self.creator = creator # username
        self.participants = [creator] # List of usernames
        self.first_matches = [] # usernames
        self.final_matches = [] # usernames
        self.played_games_count = 0

    def add_participant(self, participant):
        self.participants.append(participant)

    def create_first_matches(self):
        if len(self.participants) % 2 != 0:
            self.participants.append("AI Bot")

        random.shuffle(self.participants)

        for i in range(0, len(self.participants), 2):
            # Create a game object with the two participants
            match = (self.participants[i], self.participants[i+1])
            self.first_matches.append(match)

        self.return_first_matches()

    def add_winner_to_final_matches(self, winner):
        self.final_matches.append(winner)
        self.played_games_count += 1

    def return_first_matches(self):
        return self.first_matches
    
    def return_final_matches(self):
        return self.final_matches