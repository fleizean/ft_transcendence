#pong.py

# Define some constants for the pong game
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_SPEED = 10
BALL_SPEED = 5

# Define some variables for the game state
ballX = WIDTH / 2 - BALL_RADIUS # initial ball x position
ballY = HEIGHT / 2 - BALL_RADIUS # initial ball y position
ballVX = BALL_SPEED # initial ball x velocity
ballVY = BALL_SPEED # initial ball y velocity
paddle1Y = HEIGHT / 2 - PAD_HEIGHT / 2 # initial paddle 1 y position
paddle2Y = HEIGHT / 2 - PAD_HEIGHT / 2 # initial paddle 2 y position
paddle1VY = 0 # initial paddle 1 y velocity
paddle2VY = 0 # initial paddle 2 y velocity
player1ScoreValue = 0 # initial player 1 score
player2ScoreValue = 0 # initial player 2 score
gameState = "serve" # initial game state


# Define a function to update the game state
def update():
  # Move the ball according to its velocity
  ballX += ballVX
  ballY += ballVY
  sendballMoveEvent(ballX, ballY)

  # Check for collision with the top and bottom edges of the board
  if ballY < 0 or ballY > HEIGHT - BALL_RADIUS * 2:
    # Reverse the ball y velocity
    ballVY *= -1
    sendWallHitEvent()

  # Check for collision with the left and right edges of the board
  if (ballX < 0 or ballX > WIDTH - BALL_RADIUS * 2):
    # Increase the score of the opposite player
    if (ballX < 0):
      player2ScoreValue+= 1
    else:
      player1ScoreValue+= 1
    # Update the score display
    #player1Score.textContent = player1ScoreValue;
    #player2Score.textContent = player2ScoreValue;
    # Reset the ball position and velocity
    ballX = WIDTH / 2 - BALL_RADIUS
    ballY = HEIGHT / 2 - BALL_RADIUS
    ballVX = BALL_SPEED
    ballVY = BALL_SPEED
    # Change the game state to serve
    gameState = "serve"
    # Show a message to press enter to play
    ##message.textContent = "Press Enter to Play Pong";
    sendScoredEvent(player1ScoreValue, player2ScoreValue)
  

  # Check for collision with the paddles
  if (
    (ballX < PAD_WIDTH and ballY + BALL_RADIUS * 2 > paddle1Y and ballY < paddle1Y + PAD_HEIGHT) or
    (ballX > WIDTH - PAD_WIDTH - BALL_RADIUS * 2 and ballY + BALL_RADIUS * 2 > paddle2Y and ballY < paddle2Y + PAD_HEIGHT)
  ):
    # Reverse the ball x velocity
    ballVX *= -1;
    sendPaddleHitEvent()
  


  # Check for collision with the top and bottom edges of the board
  if (paddle1Y < 0 or paddle1Y > HEIGHT - PAD_HEIGHT):
    # Reverse the paddle 1 y velocity
    paddle1VY *= -1
  
  if (paddle2Y < 0 or paddle2Y > HEIGHT - PAD_HEIGHT):
    # Reverse the paddle 2 y velocity
    paddle2VY *= -1
  
  # Move the paddles according to their velocity
  paddle1Y += paddle1VY
  paddle2Y += paddle2VY
  sendPaddleMoveEvent(paddle1Y, paddle2Y)

  # Update the ball and paddles positions in the HTML
  # ball.style.left = ballX + "px"
  # ball.style.top = ballY + "px"
  # paddle1.style.top = paddle1Y + "px"
  # paddle2.style.top = paddle2Y + "px"
