// Create the canvas
/* var canvas = document.createElement("canvas"); */
const canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;
//document.body.appendChild(canvas);

const username = document.querySelector('.container-top').dataset.username;
const ainame = document.querySelector('.container-top').dataset.ainame;

/* Cordinates of the canvas */
var textWidth1 = ctx.measureText(username + ": " + score1).width;
var textWidth2 = ctx.measureText(ainame + ": " + score2).width;

var usernameX = 10;
var usernameY = 20;

// ainame metni sağ üst köşede
var ainameX = canvas.width - textWidth2 - 10;
var ainameY = 20;


// Paddle objects
var paddleWidth = 10;
var paddleHeight = 100;
var paddleSpeed = 15;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};


// Ball object
var ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10, speed: 5, dx: 1, dy: 1};

// Scores
var score1 = 0;
var score2 = 0;

const MAX_SCORE = 10;

// Add a new variable to track if the game is paused
let isScored = false;
var isPaused = false;
let upPressed = false;
let downPressed = false;
let upPressedAI = false;
let downPressedAI = false;
// Add a new variable for AI's target position
let moveThreshold = 8;
let targetY = paddle2.y;

// Update the ball and paddle positions
function update() {
    // If the game is paused, don't update anything
    if (isPaused) return;

    ball.x += ball.speed * ball.dx;
    ball.y += ball.speed * ball.dy;

    // Check for collisions with paddles
    if (ball.y + ball.radius > paddle1.y && ball.y - ball.radius < paddle1.y + paddle1.height && ball.dx < 0) {
        if (ball.x - ball.radius < paddle1.x + paddle1.width) {
            ball.dx *= -1;
            // Check if the ball hit the top or bottom 10% of the paddle
            if (ball.y < paddle1.y + 0.1 * paddle1.height || ball.y > paddle1.y + 0.9 * paddle1.height) {
                ball.speed *= 1.2; // Increase speed by 20%
                paddleSpeed *= 1.2;
            }
        }
    }
    if (ball.y + ball.radius > paddle2.y && ball.y - ball.radius < paddle2.y + paddle2.height && ball.dx > 0) {
        if (ball.x + ball.radius > paddle2.x) {
            ball.dx *= -1;
            // Check if the ball hit the top or bottom 10% of the paddle
            if (ball.y < paddle2.y + 0.1 * paddle2.height || ball.y > paddle2.y + 0.9 * paddle2.height) {
                ball.speed *= 1.2; // Increase speed by 20%
                paddleSpeed *= 1.2;
            }
        }
    }

    // Check for collisions with top/bottom walls
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.dy *= -1;
    }

    // Check for collisions with left/right walls (scoring)
    if (ball.x + ball.radius > canvas.width) {
        score1++;
        resetBall();
    } else if (ball.x - ball.radius < 0) {
        score2++;
        resetBall();
    }

    // Check for game over
    if (score1 == MAX_SCORE || score2 == MAX_SCORE) {
        if (score1 == MAX_SCORE) {
            alert(username + " wins!");
        } else {
            alert(ainame + " wins!");
        }
        score1 = 0;
        score2 = 0;
    }

    // Move the paddles
    if (upPressed && paddle1.y > 0 && !isScored) {
        paddle1.y -= paddle1.dy;
    } else if (downPressed && paddle1.y < canvas.height - paddle1.height && !isScored) {
        paddle1.y += paddle1.dy;
    }

    // Move the AI paddle towards the target position
    if (targetY < paddle2.y - moveThreshold && paddle2.y > 0 && !isScored) {
        paddle2.y -= paddle2.dy;
    } else if (targetY > paddle2.y + moveThreshold && paddle2.y < canvas.height - paddle2.height && !isScored) {
        paddle2.y += paddle2.dy;
    }

    // Prevent the paddles from moving off the canvas
    if (paddle1.y < 0) {
        paddle1.y = 0;
    } else if (paddle1.y > canvas.height - paddle1.height) {
        paddle1.y = canvas.height - paddle1.height;
    }
    if (paddle2.y < 0) {
        paddle2.y = 0;
    } else if (paddle2.y > canvas.height - paddle2.height) {
        paddle2.y = canvas.height - paddle2.height;
    }
}

// Draw everything
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the middle dotted line
    ctx.beginPath();
    ctx.setLineDash([5, 15]);
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = "#0095DD";
    ctx.stroke();

    // Draw the middle dotted circle
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 50, 0, Math.PI * 2, false);
    ctx.setLineDash([5, 15]);
    ctx.strokeStyle = "#0095DD";
    ctx.stroke();

    ctx.fillStyle = "#0095DD";
    ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2, false);
    ctx.fill();
    ctx.closePath();

    ctx.font = "16px Roboto";
    ctx.fillText(username + ": " + score1, usernameX, usernameY);
    ctx.fillText(ainame + ": " + score2, ainameX, ainameY);
}

// The main game loop
var main = function () {
    
    // Request to do this again ASAP
    if (!isPaused) {
        update();
        render();
    }
    requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
main();

// Reset the ball to the center
function resetBall() {
    isPaused = true; // Pause the game
    isScored = true;
    ball.speed = 5;
    paddleSpeed = 14;
    ball.dx = -ball.dx;
    ball.dy = -ball.dy;
    setTimeout(function() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        isPaused = false; // Unpause the game
    }, 500); // Wait for 0.5 second

    isPaused = true; // Pause the game
    setTimeout(function() {
        isScored = false;
        isPaused = false; // Unpause the game
    }, 1000); // Wait for 1 seconds
}

// Control paddle1 with w, s keys
document.addEventListener("keydown", function(event) {
    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
        upPressed = true;
    } else if (event.key === "s" || event.key === "S" || event.key === "ArrowDown") {
        downPressed = true;
    }
});

document.addEventListener("keyup", function(event) {
    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
        upPressed = false;
    } else if (event.key === "s" || event.key === "S" || event.key === "ArrowDown") {
        downPressed = false;
    }
});

/* // Ai Player
let errorProbability = 0.05; // 5% chance to make a mistake

setInterval(() => {
    let shouldMoveUp = Math.random() < errorProbability ? true : false;
    if (ball.y < paddle2.y && !shouldMoveUp) {
        paddle2.y -= paddle2.dy;
    } else if (ball.y > paddle2.y && !shouldMoveUp) {
        paddle2.y += paddle2.dy;
    } else {
        // Occasionally move in the opposite direction
        paddle2.y += shouldMoveUp ? -paddle2.dy : paddle2.dy;
    }
}, 100); */

/* // Ai Player
let errorProbability = 0.05; // 5% chance to make a mistake

let lastBallPosition = { x: ball.x, y: ball.y };
let ballDirection = { x: 0, y: 0 };

setInterval(() => {
    // Calculate ball direction
    ballDirection.x = ball.x - lastBallPosition.x;
    ballDirection.y = ball.y - lastBallPosition.y;

    // Predict ball's y position when it reaches the paddle
    let timeToReachPaddle = (paddle2.x - ball.x) / ballDirection.x;
    let predictedY = ball.y + ballDirection.y * timeToReachPaddle;

    // Clamp prediction within canvas
    predictedY = Math.max(0, Math.min(600, predictedY));

    // Decide whether to move up or down
    let shouldMoveUp = Math.random() < errorProbability ? true : false;
    if (predictedY < paddle2.y && !shouldMoveUp) {
        paddle2.y -= paddle2.dy;
    } else if (predictedY > paddle2.y && !shouldMoveUp) {
        paddle2.y += paddle2.dy;
    } else {
        // Occasionally move in the opposite direction
        paddle2.y += shouldMoveUp ? -paddle2.dy : paddle2.dy;
    }

    // Update last ball position
    lastBallPosition = { x: ball.x, y: ball.y };
}, 100); */

// Ai Player
let reactionDelay = 1000 / ball.speed; // Delay in milliseconds
let lastBallPosition = { x: ball.x, y: ball.y };
let ballDirection = { x: 0, y: 0 };
let predictedY = paddle2.y;

setInterval(() => {
    // Calculate ball direction
    ballDirection.x = ball.x - lastBallPosition.x;
    ballDirection.y = ball.y - lastBallPosition.y;

    // Predict ball's y position when it reaches the paddle
    let timeToReachPaddle = (paddle2.x - ball.x) / ballDirection.x;
    predictedY = ball.y + ballDirection.y * timeToReachPaddle;

    // Clamp prediction within canvas
    predictedY = Math.max(0, Math.min(canvas.height, predictedY));

    // Update last ball position
    lastBallPosition = { x: ball.x, y: ball.y };

    // Update AI paddle movement variables based on predicted position
    upPressedAI = predictedY < paddle2.y;
    downPressedAI = predictedY > paddle2.y;

    targetY = predictedY - paddle2.height / 2;
}, reactionDelay);

/* setInterval(() => {
    // Move the AI paddle
    if (upPressedAI && paddle2.y > 0) {
        paddle2.y -= paddle2.dy;
    } else if (downPressedAI && paddle2.y < canvas.height - paddle2.height) {
        paddle2.y += paddle2.dy;
    }
}, 100); */

/* setInterval(() => {
    // Move the paddle smoothly towards the predicted position
    if (predictedY < paddle2.y) {
        paddle2.y -= paddle2.dy;
    } else if (predictedY > paddle2.y) {
        paddle2.y += paddle2.dy;
    }
}, reactionDelay); */