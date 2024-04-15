from enum import Enum
import random, threading, time

WIDTH = 800
HEIGHT = 600

PAD_WIDTH = 10
PAD_HEIGHT = 100
PAD_SPEED = 15
PADDLE_Y = (HEIGHT - PAD_HEIGHT) / 2 

BALL_RADIUS = 10
BALL_SPEED = 2

MAX_SCORE = 3

class Status(Enum):
    ACCEPTED = 0
    WAITING = 1
    PLAYING = 2
    PAUSED = 3
    ENDED = 4


class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.dx = 1
        self.dy = random.choice([-1, 1])

class Paddle:
    def __init__(self, x, y, width, height, dy):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dy = dy

# Player class have username and score and Paddle object
class Player:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.paddle = None

# Game class have one Ball and two Players objects
class PongGame:
    def __init__(self, player1, player2, tournament_id=None):
        self.status = Status.ACCEPTED
        self.group_name = player1 + "-" + player2
        self.tournament_id = tournament_id
        self.ball = Ball()
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.player1.paddle = Paddle(0, PADDLE_Y, PAD_WIDTH, PAD_HEIGHT, PAD_SPEED)
        self.player2.paddle = Paddle(WIDTH - PAD_WIDTH, PADDLE_Y, PAD_WIDTH, PAD_HEIGHT, PAD_SPEED)
        self.no_more = False
        self.rageofFire = False
        self.frozenBall = False
        self.start_time = 0
        self.end_time = 0

    def moveBall(self):
        if (self.start_time == 0):
            self.start_time = time.time()

        if (self.frozenBall): return self.ball.x, self.ball.y, self.player1.score, self.player2.score
        self.ball.x += self.ball.speed * self.ball.dx
        self.ball.y += self.ball.speed * self.ball.dy

        # Check for collisions with paddles
        if self.ball.y + self.ball.radius >= self.player1.paddle.y and self.ball.y - self.ball.radius <= self.player1.paddle.y + self.player1.paddle.height and self.ball.dx < 0:
            if self.ball.x - self.ball.radius <= self.player1.paddle.x + self.player1.paddle.width:
                if self.rageofFire == True and random.random() < 0.5:
                    self.ball.speed += 0.25
                self.ball.x = self.player1.paddle.x + self.player1.paddle.width + self.ball.radius
                self.ball.dx *= -1
                if self.ball.y < self.player1.paddle.y + 0.2 * self.player1.paddle.height or self.ball.y > self.player1.paddle.y + 0.8 * self.player1.paddle.height:
                    self.ball.speed *= 1.2 # Increase speed by 20%
                    self.player1.paddle.dy *= 1.2
                    self.player2.paddle.dy *= 1.2
            

        elif self.ball.y + self.ball.radius >= self.player2.paddle.y and self.ball.y - self.ball.radius <= self.player2.paddle.y + self.player2.paddle.height and self.ball.dx > 0:
            if self.ball.x + self.ball.radius >= self.player2.paddle.x:
                if self.rageofFire == True and random.random() < 0.5:
                    self.ball.speed += 0.25
                self.ball.x = self.player2.paddle.x - self.ball.radius
                self.ball.dx *= -1
                if self.ball.y < self.player2.paddle.y + 0.2 * self.player2.paddle.height or self.ball.y > self.player2.paddle.y + 0.8 * self.player2.paddle.height:
                    self.ball.speed *= 1.2 # Increase speed by 20%
                    self.player1.paddle.dy *= 1.2
                    self.player2.paddle.dy *= 1.2
            
        # Check for collisions with top/bottom walls
        if self.ball.y + self.ball.radius > HEIGHT or self.ball.y - self.ball.radius < 0:
            self.ball.dy *= -1
        # Check for collisions with left/right walls (scoring)
        if self.ball.x + self.ball.radius > WIDTH:
            self.player1.score += 1
            self.resetBall()
        elif self.ball.x - self.ball.radius < 0:
            self.player2.score += 1
            self.resetBall()
        return self.ball.x, self.ball.y, self.player1.score, self.player2.score
    

    def movePaddle(self, player, direction):
        # Move the paddles
        mover = player == self.player1.username and self.player1 or self.player2
        if direction == "up":
            mover.paddle.y -= mover.paddle.dy
            if mover.paddle.y < 0:
                mover.paddle.y = 0
        elif direction == "down":
            mover.paddle.y += mover.paddle.dy
            if mover.paddle.y > HEIGHT - mover.paddle.height:
                mover.paddle.y = HEIGHT - mover.paddle.height
        return mover.paddle.y

    def resetBall(self):
        self.freezeGame(0.5)
        self.ball.x = WIDTH / 2
        self.ball.y = HEIGHT / 2
        self.ball.speed = 2
        self.player1.paddle.dy = PAD_SPEED
        self.player2.paddle.dy = PAD_SPEED
        self.ball.dx *= -1
        self.ball.dy = random.choice([-1, 1])
        if self.player1.score >= MAX_SCORE or self.player2.score >= MAX_SCORE:
            self.status = Status.ENDED
            self.end_time = time.time()
            #? Record the game in the database?

    def pauseGame(self):
        self.status = Status.PAUSED

    def resumeGame(self):
        self.status = Status.PLAYING

    def freezeGame(self, second):
        self.frozenBall = True
        def unfreeze_ball():
            self.frozenBall = False

        threading.Timer(second, unfreeze_ball).start()


    def activateAbility(self, username, ability):
        if ability == "frozenBall":
            # Topu 3 saniyeliğine durdurur
            self.freezeGame(3)

        elif ability == "fastandFurious":
            # Topu 5 kat hızlandırır
            self.ball.speed *= 5
        elif ability == "likeaCheater": 
            # Rakibinin 1 puanını gasp eder
            if (self.player1.username == username):
                if self.player2.score > 0:
                    self.player2.score -= 1
                self.player1.score += 1
            else:
                if self.player1.score > 0:
                    self.player1.score -= 1
                self.player2.score += 1
        elif ability == "rageofFire": 
            # Her paddle'a dokunuşta +0.25 topu hızlandır
            self.rageofFire = True
        elif ability == "giantMan":  
            if (self.player1.username == username):
                self.player1.paddle.height = 115
            else:
                self.player2.paddle.height = 115

    def otherPlayer(self, username):
        if username == self.player1.username:
            return self.player2.username
        else:
            return self.player1.username
        
    def getWinnerLoserandScores(self):
        if self.player1.score > self.player2.score:
            return self.player1.username, self.player2.username, self.player1.score, self.player2.score
        else:
            return self.player2.username, self.player1.username, self.player2.score, self.player1.score

    def getScore(self, username):
        if username == self.player1.username:
            return self.player1.score
        else:
            return self.player2.score

    def getDuration(self):
        if self.start_time == 0:
            return 0
        if self.end_time == 0:
            self.end_time = time.time()
        return self.end_time - self.start_time 


