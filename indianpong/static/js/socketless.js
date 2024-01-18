// Create the canvas
/* var canvas = document.createElement("canvas"); */
const canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;
//document.body.appendChild(canvas);

// Paddle objects
var paddleWidth = 10;
var paddleHeight = 75;
var paddleSpeed = 50;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};

// Ball object
var ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10, speed: 2, dx: 1, dy: 1};

// Scores
var score1 = 0;
var score2 = 0;

// Update the ball and paddle positions
function update() {
    ball.x += ball.speed * ball.dx;
    ball.y += ball.speed * ball.dy;

    // Check for collisions with paddles
    if (ball.y + ball.radius > paddle1.y && ball.y - ball.radius < paddle1.y + paddle1.height && ball.dx < 0) {
        if (ball.x - ball.radius < paddle1.x + paddle1.width) {
            ball.dx *= -1;
        }
    }
    if (ball.y + ball.radius > paddle2.y && ball.y - ball.radius < paddle2.y + paddle2.height && ball.dx > 0) {
        if (ball.x + ball.radius > paddle2.x) {
            ball.dx *= -1;
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

    // Move the paddles
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

    ctx.fillStyle = "#0095DD";
    ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2, false);
    ctx.fill();
    ctx.closePath();

    ctx.font = "16px Arial";
    ctx.fillText("Player 1: " + score1, 10, 20);
    ctx.fillText("Player 2: " + score2, canvas.width - 85, 20);
}

// The main game loop
var main = function () {
    update();
    render();

    // Request to do this again ASAP
    requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
main();

// Reset the ball to the center
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 2;
    ball.dx = -ball.dx;
    ball.dy = -ball.dy;
}
// Control paddle1 with w, s keys
document.addEventListener("keydown", function(event) {
    if (event.key === "w") {
        paddle1.y -= paddle1.dy;
    } else if (event.key === "s") {
        paddle1.y += paddle1.dy;
    }
});

// Control paddle2 with u, j keys
document.addEventListener("keydown", function(event) {
    if (event.key === "u") {
        paddle2.y -= paddle2.dy;
    } else if (event.key === "j") {
        paddle2.y += paddle2.dy;
    }
});
