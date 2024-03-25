from enum import Enum

class Choices(Enum):
    ROCK = 0
    PAPER = 1
    SCISSOR = 2
    LIKEACHEATER = 3
    GODOFTHINGS = 4

class RoundResult(Enum):
    DRAW = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    OVER = 3

KV_CHOICES = {'rock': Choices.ROCK, 'paper': Choices.PAPER, 'scissor': Choices.SCISSOR}

class Shaker:
    def __init__(self, username):
        self.username = username
        self.max_score = 3
        self.score = 0
        self.choices = []

class RPS:
    def __init__(self, player1, player2):
        self.shaker1 = Shaker(player1)
        self.shaker2 = Shaker(player2)
        self.group_name = f'rps_{player1}_{player2}'

    def play(self, username, choice):
        if username == self.shaker1.username:
            self.shaker1.choices.append(KV_CHOICES[choice])
        elif username == self.shaker2.username:
            self.shaker2.choices.append(KV_CHOICES[choice])

    def round_result(self):
        if self.shaker1.score == self.shaker1.max_score or self.shaker2.score == self.shaker2.max_score:
            return RoundResult.OVER
        result = (self.shaker1.choices.pop().value - self.shaker2.choices.pop().value) % 3
        if result == 0:
            return RoundResult.DRAW
        elif result == 1:
            self.shaker1.score += 1
            return RoundResult.PLAYER1_WIN
        else:
            self.shaker2.score += 1
            return RoundResult.PLAYER2_WIN

    def get_winner_loser(self):
        if self.shaker1.score > self.shaker2.score:
            return self.shaker1.username, self.shaker2.username
        else:
            return self.shaker2.username, self.shaker1.username

    def get_score(self):
        return self.shaker1.score, self.shaker2.score

