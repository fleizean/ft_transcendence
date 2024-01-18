// Create the canvas
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;
document.body.appendChild(canvas);

// Paddle objects
var paddleWidth = 10;
var paddleHeight = 75;
var paddleSpeed = 2;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: paddleHeight, dy: paddleSpeed};

// Ball object
var ballRadius = 10;
var ball = {x: canvas.width / 2, y: canvas.height / 2, speed: 2, dx: 1, dy: 1};

// Scores
var score1 = 0;
var score2 = 0;

// WebSocket connection
var socket = new WebSocket('ws://localhost:8000/ws/pong/');

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.type === 'ball_update') {
        ball = data.ball;
    }
};

// Key press state
var keys = {};

window.addEventListener('keydown', function(event) {
    keys[event.key] = true;
});

window.addEventListener('keyup', function(event) {
    keys[event.key] = false;
});

// Update the paddle positions
function updatePaddles() {
    if (keys['w']) {
        paddle1.y -= paddle1.dy;
    }
    if (keys['s']) {
        paddle1.y += paddle1.dy;
    }
    if (keys['ArrowUp']) {
        paddle2.y -= paddle2.dy;
    }
    if (keys['ArrowDown']) {
        paddle2.y += paddle2.dy;
    }
}

// Draw everything
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#0095DD";
    ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI*2, false);
    ctx.fill();
    ctx.closePath();

    ctx.font = "16px Arial";
    ctx.fillText("Player 1: " + score1, 10, 20);
    ctx.fillText("Player 2: " + score2, canvas.width - 85, 20);
}

// The main game loop
var main = function () {
    updatePaddles();
    render();

    // Request to do this again ASAP
    requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
main();