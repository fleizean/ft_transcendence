
const canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;


const canvasContainer = document.querySelector('.ai-game');

const username = document.querySelector('.container-top').dataset.username;
const player2name = document.querySelector('.container-top').dataset.player2name;
const paddleColor = document.querySelector('.container-top').dataset.paddlecolor;
const playgroundColor = document.querySelector('.container-top').dataset.playgroundcolor;
canvas.style.borderColor = playgroundColor; // Set the border color to the specified color

// Pong Abilities
const giantMan = document.querySelector('.container-top').dataset.giantman;
const likeaCheater = document.querySelector('.container-top').dataset.likeacheater;
const fastandFurious = document.querySelector('.container-top').dataset.fastandfurious;
const rageofFire = document.querySelector('.container-top').dataset.rageoffire;
const frozenBall = document.querySelector('.container-top').dataset.frozenball;

/* Cordinates of the canvas */
var textWidth1 = ctx.measureText(username + ": " + score1).width;
var textWidth2 = ctx.measureText(player2name + ": " + score2).width;


var usernameX = 10;
var usernameY = 20;
// player2 metni sağ üst köşede
var player2nameX = canvas.width - textWidth2 - 10;
var player2nameY = 20;

// if giantMan abilities equiped
var abilities_paddleHeight = (giantMan == "true") ? 115 : 100;
var paddleWidth = 10;
var paddleHeight = 100;
var paddleSpeed = 15;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};

// Ball object
var ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10, speed: 5, dx: 1, dy: 1};

// Scores
var score1 = 0;
var score2 = 0;

const MAX_SCORE = 3;

// Player Abilities
var likeaCheaterCount = 0;
var fastandFuriousCount = 0;
var frozenBallCount = 0;
var Player2FrozenBallCount = 0;
var Player2LikeaCheaterCount = 0;
var Player2FastandFuriousCount = 0;

var isFrozenBallActive = false;

// Add a new variable to track if the game is paused
let isScored = false;
var isPaused = false;
let upPressed = false;
let downPressed = false;
let upPressedPlayer2 = false;
let downPressedPlayer2 = false;


function resetAbilities() {
    likeaCheaterCount = 0;
    fastandFuriousCount = 0;
    frozenBallCount = 0;
    Player2FrozenBallCount = 0;
    Player2LikeaCheaterCount = 0;
    Player2FastandFuriousCount = 0;
}

// Update the ball and paddle positions
function update() {
    // If the game is paused, don't update anything
    if (isPaused) return;

    ball.x += ball.speed * ball.dx;
    ball.y += ball.speed * ball.dy;

    // Check for collisions with paddles
    if (ball.y + ball.radius > paddle1.y && ball.y - ball.radius < paddle1.y + paddle1.height && ball.dx < 0) {       
        if (ball.x - ball.radius < paddle1.x + paddle1.width) {
            if (rageofFire == "true") {
                if (Math.random() <= 0.5) {
                    ball.speed += 1;
                }
            }
            ball.dx *= -1;
            // Check if the ball hit the top or bottom 20% of the paddle
            if (ball.y < paddle1.y + 0.2 * paddle1.height || ball.y > paddle1.y + 0.8 * paddle1.height) {
                ball.speed *= 1.2; // Increase speed by 20%
                paddleSpeed *= 1.2;
            }
        }
    }
    if (ball.y + ball.radius > paddle2.y && ball.y - ball.radius < paddle2.y + paddle2.height && ball.dx > 0) {
        if (ball.x + ball.radius > paddle2.x) {
            if (rageofFire == "true") {
                if (Math.random() <= 0.5) {
                    ball.speed += 1;
                }
            }
            ball.dx *= -1;
            // Check if the ball hit the top or bottom 20% of the paddle
            if (ball.y < paddle2.y + 0.2 * paddle2.height || ball.y > paddle2.y + 0.8 * paddle2.height) {
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
        showGameOverScreen();
    }

    // Move the paddle1
    if (upPressed && paddle1.y > 0 && !isScored) {
        paddle1.y -= paddle1.dy;
    } else if (downPressed && paddle1.y < canvas.height - paddle1.height && !isScored) {
        paddle1.y += paddle1.dy;
    }

    // Move the paddle2
    if (upPressedPlayer2 && paddle2.y > 0 && !isScored) { 
        paddle2.y -= paddle2.dy;
    } else if (downPressedPlayer2 && paddle2.y < canvas.height - paddle2.height && !isScored) {
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

/// Draw everything
function render() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Create a radial gradient for the background
    var gradient = ctx.createRadialGradient(canvas.width / 2, canvas.height / 2, 10, canvas.width / 2, canvas.height / 2, 300);
    gradient.addColorStop(0, 'lightgrey');
    gradient.addColorStop(1, 'darkgrey');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw the middle dotted line
    ctx.beginPath();
    ctx.setLineDash([5, 15]);
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = "black";
    ctx.stroke();

    // Draw the middle dotted circle
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 50, 0, Math.PI * 2, false);
    ctx.setLineDash([5, 15]);
    ctx.stroke();

    // Add shiny effect to the ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2, false);
    var gradient = ctx.createRadialGradient(ball.x, ball.y, 0, ball.x, ball.y, ball.radius);
    gradient.addColorStop(0, 'white');
    gradient.addColorStop(0.1, 'gold');
    gradient.addColorStop(1, 'darkorange');
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.closePath();

    // Add shadow to the paddles
    ctx.shadowColor = 'black';
    ctx.shadowBlur = 10;
    ctx.shadowOffsetX = 5;
    ctx.shadowOffsetY = 5;


    ctx.fillStyle = paddleColor
    ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    // If paddle2 is on the right, draw the shadow to the left
    ctx.shadowOffsetX = -5;
    ctx.shadowOffsetY = 5;
    ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);


    // Reset shadow properties
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    ctx.font = "16px Roboto";
    ctx.fillStyle = 'white';
    ctx.fillText(username + ": " + score1, usernameX, usernameY);
    ctx.fillText(player2name + ": " + score2, player2nameX, player2nameY);
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
    isScored = true;
    isPaused = true;
    ball.speed = 5;
    paddleSpeed = 14;
    ball.dx = -ball.dx;
    ball.dy = -ball.dy;
    setTimeout(() => {     
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        isPaused = false;
        isScored = false;
    }, 500);
}

function frozenBallAbility() {
    var nowBallSpeed = ball.speed;
    isFrozenBallActive = true;
    ball.speed = 0;
    setTimeout(function() {
        ball.speed = nowBallSpeed;
        isFrozenBallActive = false;
    }, 2000);
}

function likeaCheaterAbility(isPlayer2) {
    if (isPlayer2) {
        score2++;
        if (score1 > 0) {
            score1--;
        }
    }
    else {
        score1++;
        if (score2 > 0) {
            score2--;
        }
    }
}

function fastandFuriousAbility() {
    ball.speed += 10;
}

// Control paddle1 with w, s keys
document.addEventListener("keydown", function(event) {
    if (event.key === "w" || event.key === "W") {
        upPressed = true;
    } 
    else if (event.key === "s" || event.key === "S") {
        downPressed = true;
    }
    else if (event.key === '1' && likeaCheaterCount < 1 && likeaCheater == "true") {
        likeaCheaterAbility();
        likeaCheaterCount += 1;
    }
    else if (event.key === '2' && fastandFuriousCount < 1 && fastandFurious == "true" && isFrozenBallActive == false) {
        fastandFuriousAbility();
        fastandFuriousCount += 1;
    }
    else if (event.key === '3' && frozenBallCount < 1 && frozenBall == "true") {
        frozenBallAbility();
        frozenBallCount += 1;
    }
});

// Control paddle2 with arrow keys
document.addEventListener("keydown", function(event) {
    if (event.key === "ArrowUp") {
        upPressedPlayer2 = true;
    } else if (event.key === "ArrowDown") {
        downPressedPlayer2 = true;
    }
    else if (event.key === '8' && Player2LikeaCheaterCount < 1 && likeaCheater == "true") {
        likeaCheaterAbility(true);
        Player2LikeaCheaterCount += 1;
    }
    else if (event.key === '9' && Player2FastandFuriousCount < 1 && fastandFurious == "true" && isFrozenBallActive == false) {
        fastandFuriousAbility();
        Player2FastandFuriousCount += 1;
    }
    else if (event.key === '0' && Player2FrozenBallCount < 1 && frozenBall == "true") {
        frozenBallAbility();
        Player2FrozenBallCount += 1;
    }
});

document.addEventListener("keyup", function(event) {
    if (event.key === "w" || event.key === "W" ) {
        upPressed = false;
    } else if (event.key === "s" || event.key === "S") {
        downPressed = false;
    }
});

document.addEventListener("keyup", function(event) {
    if (event.key === "ArrowUp") {
        upPressedPlayer2 = false;
    } else if (event.key === "ArrowDown") {
        downPressedPlayer2 = false;
    }
});


// Reset the paddle1 position?
function resetPaddles() {
    paddle1.y = (canvas.height - abilities_paddleHeight) / 2; 
    paddle2.y = (canvas.height - abilities_paddleHeight) / 2;
}

function resetGame() {
    score1 = 0;
    score2 = 0;
    resetBall();
    resetPaddles();
    resetAbilities();
}


// Oyun bitiş ekranını gösteren fonksiyon
function showGameOverScreen() {
    isPaused = true;
    var winnerText = (score1 == MAX_SCORE) ? username + " wins!" : player2name + " wins!";
    document.getElementById('winnerText').innerText = winnerText;
    document.getElementById('gameOverScreen').style.display = 'block';
}

// Oyunu tekrar başlatan fonksiyon
function restartGame() {
    document.getElementById('gameOverScreen').style.display = 'none';
    resetGame();
    //isPaused = false;
}

// Çıkış yapma işlemleri
function exitGame() {
    window.location.href = '/dashboard';
}

document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('exitButton').addEventListener('click', exitGame);
