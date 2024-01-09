import random

WIDTH = 800
HEIGHT = 600

PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_SPEED = 50
PADDLE_Y = (HEIGHT - PAD_HEIGHT) / 2 

BALL_RADIUS = 20
BALL_SPEED = 5

class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.dx = random.choice([-1, 1])
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
        self.paddle = Paddle()

# Game class have one Ball and two Players objects
class Game:
    def __init__(self, player1, player2):
        self.ball = Ball()
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.player1.paddle =Paddle(0, PADDLE_Y, PAD_WIDTH, PAD_HEIGHT, PAD_SPEED)
        self.player2.paddle = Paddle(WIDTH - PAD_WIDTH, PADDLE_Y, PAD_WIDTH, PAD_HEIGHT, PAD_SPEED)

    def moveBall(self):
        self.ball.x += self.ball.speed * self.ball.dx
        self.ball.y += self.ball.speed * self.ball.dy

        # Check for collisions with paddles
        if self.ball.y + self.ball.radius > self.player1.paddle.y and self.ball.y - self.ball.radius < self.player1.paddle.y + self.player1.paddle.height and self.ball.dx < 0:
            if self.ball.x - self.ball.radius < self.player1.paddle.x + self.player1.paddle.width:
                self.ball.dx *= -1

        if self.ball.y + self.ball.radius > self.player2.paddle.y and self.ball.y - self.ball.radius < self.player2.paddle.y + self.player2.paddle.height and self.ball.dx > 0:
            if self.ball.x + self.ball.radius > self.player2.paddle.x:
                self.ball.dx *= -1

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
        return self.ball.x, self.ball.y
    

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
        self.ball.x = WIDTH / 2
        self.ball.y = HEIGHT / 2
        self.ball.dx = random.choice([-1, 1])
        self.ball.dy = random.choice([-1, 1])



