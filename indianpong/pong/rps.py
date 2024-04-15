from enum import Enum
import time

class Choices(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Abilities(Enum):
    LIKEACHEATER = 3,
    GODOFTHINGS = 4

class RoundResult(Enum):
    DRAW = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2

KV_CHOICES = {'rock': Choices.ROCK, 'paper': Choices.PAPER, 'scissors': Choices.SCISSORS, 'godthings': Abilities.GODOFTHINGS, 'cheater': Abilities.LIKEACHEATER}

class Shaker:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.choices = []

class RPS:
    def __init__(self, player1, player2):
        self.shaker1 = Shaker(player1)
        self.shaker2 = Shaker(player2)
        self.max_score = 3
        self.group_name = f'rps_{player1}_{player2}'
        self.start_time = 0
        self.end_time = 0

    def play(self, username, choice):
        if (self.start_time == 0):
            self.start_time = time.time()
        if username == self.shaker1.username:
            self.shaker1.choices.append(KV_CHOICES[choice])
        elif username == self.shaker2.username:
            self.shaker2.choices.append(KV_CHOICES[choice])

    def ability_result(self, choice1, choice2):
        ab1 = choice1 == Abilities.LIKEACHEATER or choice1 == Abilities.GODOFTHINGS
        ab2 = choice2 == Abilities.LIKEACHEATER or choice2 == Abilities.GODOFTHINGS
        if ab1 and ab2:                                 #both played this it's draw
            return 0
        elif ab1 and choice1 == Abilities.LIKEACHEATER: #stole opponent score if greater than 0
            if self.shaker2.score > 0:
                self.shaker2.score -= 1
            self.shaker1.score += 1
            return 1
        elif ab2 and choice2 == Abilities.LIKEACHEATER: #won round instantly
            if self.shaker1.score > 0:
                self.shaker1.score -= 1
            self.shaker2.score += 1
            return 2
        elif ab1 and choice1 == Abilities.GODOFTHINGS:
            self.shaker1.score += 1
            return 1
        elif ab2 and choice2 == Abilities.GODOFTHINGS:
            self.shaker2.score += 1
            return 2
        else:
            return 3


    def round_result(self):
        shaker1_choice = self.shaker1.choices.pop()
        shaker2_choice = self.shaker2.choices.pop()
        result = self.ability_result(shaker1_choice, shaker2_choice) 
        if result == 0:
            return RoundResult.DRAW.name
        elif result == 1:
            return RoundResult.PLAYER1_WIN.name
        elif result == 2:
            return RoundResult.PLAYER2_WIN.name
        result = (shaker1_choice.value - shaker2_choice.value) % 3
        if result == 0:
            return RoundResult.DRAW.name
        elif result == 1:
            self.shaker1.score += 1
            return RoundResult.PLAYER1_WIN.name
        else:
            self.shaker2.score += 1
            return RoundResult.PLAYER2_WIN.name
        
    def check_is_over(self):
        if self.shaker1.score == self.max_score or self.shaker2.score == self.max_score:
            self.end_time = time.time()
            return True
        return False

    def get_winner_loser(self):
        if self.shaker1.score > self.shaker2.score:
            return self.shaker1.username, self.shaker2.username
        else:
            return self.shaker2.username, self.shaker1.username
    
    def otherPlayer(self, username):
        if username == self.shaker1.username:
            return self.shaker2.username
        else:
            return self.shaker1.username

    def get_scores(self):
        return self.shaker1.score, self.shaker2.score
    
    def getDuration(self):
        if self.start_time == 0:
            return 0
        if self.end_time == 0:
            self.end_time = time.time()
        return self.end_time - self.start_time
    
    def getWinnerLoserandScores(self):
        if self.shaker1.score > self.shaker2.score:
            return self.shaker1.username, self.shaker2.username, self.shaker1.score, self.shaker2.score
        else:
            return self.shaker2.username, self.shaker1.username, self.shaker2.score, self.shaker1.score

    def both_played(self):
        return len(self.shaker1.choices) == len(self.shaker2.choices) == 1
    
    def getChoices(self):
        return self.shaker1.choices[0].name, self.shaker2.choices[0].name
