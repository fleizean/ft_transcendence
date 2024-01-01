// pong.js
// Get references to the elements in the HTML
const board = document.querySelector(".board");
const ball = document.querySelector(".ball");
const paddle1 = document.querySelector(".paddle_1");
const paddle2 = document.querySelector(".paddle_2");
const player1Score = document.querySelector(".player_1_score");
const player2Score = document.querySelector(".player_2_score");
const message = document.querySelector(".message");

// Define some constants for the game
const boardWidth = 600;
const boardHeight = 400;
const ballSize = 20;
const paddleWidth = 10;
const paddleHeight = 80;
const paddleSpeed = 5;
const ballSpeed = 3;

// Define some variables for the game state
let ballX = boardWidth / 2 - ballSize / 2; // initial ball x position
let ballY = boardHeight / 2 - ballSize / 2; // initial ball y position
let ballVX = ballSpeed; // initial ball x velocity
let ballVY = ballSpeed; // initial ball y velocity
let paddle1Y = boardHeight / 2 - paddleHeight / 2; // initial paddle 1 y position
let paddle2Y = boardHeight / 2 - paddleHeight / 2; // initial paddle 2 y position
let paddle1VY = 0; // initial paddle 1 y velocity
let paddle2VY = 0; // initial paddle 2 y velocity
let player1ScoreValue = 0; // initial player 1 score
let player2ScoreValue = 0; // initial player 2 score
let gameState = "serve"; // initial game state

// Define a function to update the game state
function update() {
  // Move the ball according to its velocity
  ballX += ballVX;
  ballY += ballVY;

  // Check for collision with the top and bottom edges of the board
  if (ballY < 0 || ballY > boardHeight - ballSize) {
    // Reverse the ball y velocity
    ballVY *= -1;
  }

  // Check for collision with the left and right edges of the board
  if (ballX < 0 || ballX > boardWidth - ballSize) {
    // Increase the score of the opposite player
    if (ballX < 0) {
      player2ScoreValue++;
    } else {
      player1ScoreValue++;
    }
    // Update the score display
    player1Score.textContent = player1ScoreValue;
    player2Score.textContent = player2ScoreValue;
    // Reset the ball position and velocity
    ballX = boardWidth / 2 - ballSize / 2;
    ballY = boardHeight / 2 - ballSize / 2;
    ballVX = ballSpeed;
    ballVY = ballSpeed;
    // Change the game state to serve
    gameState = "serve";
    // Show a message to press enter to play
    message.textContent = "Press Enter to Play Pong";
  }

  // Check for collision with the paddles
  if (
    (ballX < paddleWidth && ballY + ballSize > paddle1Y && ballY < paddle1Y + paddleHeight) ||
    (ballX > boardWidth - paddleWidth - ballSize && ballY + ballSize > paddle2Y && ballY < paddle2Y + paddleHeight)
  ) {
    // Reverse the ball x velocity
    ballVX *= -1;
  }

  // Move the paddles according to their velocity
  paddle1Y += paddle1VY;
  paddle2Y += paddle2VY;

  // Check for collision with the top and bottom edges of the board
  if (paddle1Y < 0 || paddle1Y > boardHeight - paddleHeight) {
    // Reverse the paddle 1 y velocity
    paddle1VY *= -1;
  }
  if (paddle2Y < 0 || paddle2Y > boardHeight - paddleHeight) {
    // Reverse the paddle 2 y velocity
    paddle2VY *= -1;
  }

  // Update the ball and paddles positions in the HTML
  ball.style.left = ballX + "px";
  ball.style.top = ballY + "px";
  paddle1.style.top = paddle1Y + "px";
  paddle2.style.top = paddle2Y + "px";
}

// Define a function to handle key down events
function handleKeyDown(event) {
  // Get the key code of the pressed key
  const keyCode = event.keyCode;

  // If the game state is serve
  if (gameState === "serve") {
    // If the key is enter
    if (keyCode === 13) {
      // Change the game state to play
      gameState = "play";
      // Hide the message
      message.textContent = "";
    }
  }

  // If the game state is play
  if (gameState === "play") {
    // If the key is w
    if (keyCode === 87) {
      // Set the paddle 1 y velocity to negative paddle speed
      paddle1VY = -paddleSpeed;
    }
    // If the key is s
    if (keyCode === 83) {
      // Set the paddle 1 y velocity to positive paddle speed
      paddle1VY = paddleSpeed;
    }
    // If the key is up arrow
    if (keyCode === 38) {
      // Set the paddle 2 y velocity to negative paddle speed
      paddle2VY = -paddleSpeed;
    }
    // If the key is down arrow
    if (keyCode === 40) {
      // Set the paddle 2 y velocity to positive paddle speed
      paddle2VY = paddleSpeed;
    }
  }
}

// Define a function to handle key up events
function handleKeyUp(event) {
  // Get the key code of the released key
  const keyCode = event.keyCode;

  // If the game state is play
  if (gameState === "play") {
    // If the key is w or s
    if (keyCode === 87 || keyCode === 83) {
      // Set the paddle 1 y velocity to zero
      paddle1VY = 0;
    }
    // If the key is up arrow or down arrow
    if (keyCode === 38 || keyCode === 40) {
      // Set the paddle 2 y velocity to zero
      paddle2VY = 0;
    }
  }
}

// Add event listeners for key down and key up events
document.addEventListener("keydown", handleKeyDown);
document.addEventListener("keyup", handleKeyUp);

// Call the update function every 16 milliseconds
setInterval(update, 16);