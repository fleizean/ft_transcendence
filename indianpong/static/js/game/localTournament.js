export function localTournament() {
const canvas = document.getElementById('pongCanvas');
var gameStartInfos = document.getElementById("tournament-start-info");
var gameInfoTournament = document.getElementById("game-info-tournament");
var startButton = document.getElementById("startButton");
var startTournament = document.getElementById("startTournament");
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;


const canvasContainer = document.querySelector('.ai-game');
var gameMode = "Vanilla";

/* Tournament */
var playerNames = [];
var matches = [];
const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
const selectedLanguage = cookie ? cookie.split('=')[1] : 'en';

var matchCount = 0;

const paddleColor = document.querySelector('.container-top').dataset.paddlecolor;
const playgroundColor = document.querySelector('.container-top').dataset.playgroundcolor;
canvas.style.borderColor = playgroundColor; // Set the border color to the specified color

/* Cordinates of the canvas */
var textWidth1 = ctx.measureText(matches[matchCount] + ": " + score1).width;
var textWidth2 = ctx.measureText(matches[matchCount] + ": " + score2).width;


var usernameX = 10;
var usernameY = 20;
// player2 metni sağ üst köşede
var player2nameX = canvas.width - textWidth2 - 10;
var player2nameY = 20;

// if giantMan abilities equiped
var abilities_paddleHeight = (gameMode == "Abilities") ? 115 : 100;
var paddleWidth = 10;
var paddleHeight = 100;
var paddleSpeed = 15;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};

// Ball object
var ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10, speed: 10, dx: 1, dy: 1};

// Scores
var isGameStarted = false;

var score1 = 0;
var score2 = 0;

var MAX_SCORE = 3;

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
var isPaused = true;
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
    if (ball.y + ball.radius >= paddle1.y && ball.y - ball.radius <= paddle1.y + paddle1.height && ball.dx < 0) {       
        if (ball.x - ball.radius <= paddle1.x + paddle1.width) {
            if (gameMode == "Abilities") {
                if (Math.random() <= 0.5) {
                    ball.speed += 0.25;
                }
            }
            ball.x = paddle1.x + paddle1.width + ball.radius;
            ball.dx *= -1;
            if (ball.y < paddle1.y + 0.2 * paddle1.height || ball.y > paddle1.y + 0.8 * paddle1.height) {
                ball.speed *= 1.2; // Increase speed by 20%
                paddleSpeed *= 1.2;
            }
        }
    }
    if (ball.y + ball.radius >= paddle2.y && ball.y - ball.radius <= paddle2.y + paddle2.height && ball.dx > 0) {
        if (ball.x + ball.radius >= paddle2.x) {
            if (gameMode == "Abilities") {
                if (Math.random() <= 0.5) {
                    ball.speed += 0.25;
                }
            }
            ball.x = paddle2.x - ball.radius;
            ball.dx *= -1;
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
        if (matchCount < 2) {
            showGameOverScreen(score1 == MAX_SCORE ? matches[matchCount].player1 : matches[matchCount].player2);
        }
        else {
            isPaused = true;
            showGameOverTournament(score1 == MAX_SCORE ? matches[matchCount].player1 : matches[matchCount].player2);
        }
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

    // Reset shadow properties
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    ctx.font = "16px Roboto";
    ctx.fillStyle = 'white';
    
    
    if (matchCount === 0) {        
        ctx.fillText(matches[matchCount].player1 + ": " + score1, usernameX, usernameY);
        ctx.fillText(matches[matchCount].player2 + ": " + score2, player2nameX, player2nameY);
    }
    else if (matchCount === 1) {
        ctx.fillText(matches[matchCount].player1 + ": " + score1, usernameX, usernameY);
        ctx.fillText(matches[matchCount].player2 + ": " + score2, player2nameX, player2nameY);
    }
    else if (matchCount === 2) {
        ctx.fillText(matches[matchCount].player1 + ": " + score1, usernameX, usernameY);
        ctx.fillText(matches[matchCount].player2 + ": " + score2, player2nameX, player2nameY);
    }
}


// The main game loop
var main = function () {
    // Request to do this again ASAP
    if (!isPaused) {
        update();
        render();
    }

    localTournamentAnimationId = requestAnimationFrame(main);
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
    ball.speed = 10;
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

function likeaCheaterAbility(whichPlayer) {
    if (whichPlayer == "Player2") {
        score2++;
        if (score1 > 0) {
            score1--;
        }
    }
    else if (whichPlayer == "Player1") {
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
    else if (event.key === '1' && likeaCheaterCount < 1 && gameMode == "Abilities") {
        likeaCheaterAbility("Player1");
        likeaCheaterCount += 1;
    }
    else if (event.key === '2' && fastandFuriousCount < 1 && gameMode == "Abilities" && isFrozenBallActive == false) {
        fastandFuriousAbility();
        fastandFuriousCount += 1;
    }
    else if (event.key === '3' && frozenBallCount < 1 && gameMode == "Abilities") {
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
    else if (event.key === '8' && Player2LikeaCheaterCount < 1 && gameMode == "Abilities") {
        likeaCheaterAbility("Player2");
        Player2LikeaCheaterCount += 1;
    }
    else if (event.key === '9' && Player2FastandFuriousCount < 1 && gameMode == "Abilities" && isFrozenBallActive == false) {
        fastandFuriousAbility();
        Player2FastandFuriousCount += 1;
    }
    else if (event.key === '0' && Player2FrozenBallCount < 1 && gameMode == "Abilities") {
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

function showCanvas() {
    pongCanvas.style.display = "block";
    gameStartInfos.style.display = "none";
    gameInfoTournament.style.display = "block";
    isPaused = false;
    isGameStarted = true;
  }

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
function showGameOverScreen(player1, player2) {
    gameInfoTournament.style.display = "none";
    var message = " wins!";
    var tournamentText = "Tournament is over! ";
    if (selectedLanguage == 'hi') {
        message = " जीत!";
        tournamentText = "टूर्नामेंट ख़त्म हो गया है! ";
    }
    else if (selectedLanguage == 'pt') {
        message = " vence!";
        tournamentText = "O torneio acabou! ";
    }
    else if (selectedLanguage == 'tr') {
        message = " kazandI!";
        tournamentText = "Turnuva bitti! ";
    }
    else {
        message = " wins!";
        tournamentText = "Tournament is over! ";
    }

    var winnerText = (score1 == MAX_SCORE) ? player1 + message : player2 + message;
    document.getElementById('winnerText').innerText = winnerText;
    document.getElementById('gameOverScreen').style.display = 'block';
    var winnerName = (score1 == MAX_SCORE) ? player1 : player2;
    if (matchCount === 0) {
        var match = {
            player1: winnerName,
            player2: "Player2"
        };
        matches.push(match);
    }
    else if (matchCount === 1) {
        matches[2].player2 = winnerName;
    }
    if (isPaused == false) {
        matchCount++;
        if (matchCount === 3)
            document.getElementById('winnerText').innerText = tournamentText + winnerName + message;
    }
    isPaused = true;
}

function showGameOverTournament(winner) {
    isGameStarted = false;
    gameInfoTournament.style.display = "none";
    var winnerText = winner + " wins the tournament!";
    if (selectedLanguage === "tr") {
        winnerText = winner + " turnuvayI kazandI!";
    }
    else if (selectedLanguage === 'hi') {
        winnerText = winner + " टूर्नामेंट जीतता है!";
    }
    else if (selectedLanguage === 'pt') {
        winnerText = winner + " vence o torneio!";
    }
     
    document.getElementById('winnerTextTournament').innerText = winnerText;
    document.getElementById('gameOverScreenTournament').style.display = 'block';
}

function showBracket() {
    gameStartInfos.style.display = "none";
    canvas.style.display = "none";
    // Oyuncu isimlerini karıştır
    playerNames.sort(() => Math.random() - 0.5);
    
    // Oyuncu isimlerini rastgele çiftler oluştur
    while (playerNames.length > 1) {
        var randomIndex1 = Math.floor(Math.random() * playerNames.length);
        var player1 = playerNames[randomIndex1];
        playerNames.splice(randomIndex1, 1);
    
        var randomIndex2 = Math.floor(Math.random() * playerNames.length);
        var player2 = playerNames[randomIndex2];
        playerNames.splice(randomIndex2, 1);
    
        var match = {
            player1: player1,
            player2: player2
        };
        matches.push(match);
    }


    
    document.getElementById('top-name-1').innerText = matches[0].player1;
    document.getElementById('top-name-2').innerText = matches[0].player2;

    document.getElementById('bottom-name-1').innerText = matches[1].player1;
    document.getElementById('bottom-name-2').innerText = matches[1].player2;
    
    document.getElementById('final-name-1').innerText = matches[0].player1.substring(0,6) + " / " + matches[0].player2.substring(0,6);
    document.getElementById('final-name-2').innerText = matches[1].player1.substring(0,6) + " / " + matches[1].player2.substring(0,6);

    document.getElementById('show-bracket').style.display = 'block';
}

// Oyunu tekrar başlatan fonksiyon
function restartGame() {
    document.getElementById('gameOverScreen').style.display = 'none';
    gameInfoTournament.style.display = "block";
    resetGame();
}


// Çıkış yapma işlemleri
function exitGame() {
    swapApp('/pong-game-find')
}

document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('exitButtonTournament').addEventListener('click', exitGame);

function replaceTurkishCharacters(str) {
    var turkishMap = {
        'ş':'s', 'Ş':'S', 'ı':'i', 'İ':'I',
        'ğ':'g', 'Ğ':'G', 'ü':'u', 'Ü':'U',
        'ö':'o', 'Ö':'O', 'ç':'c', 'Ç':'C'
    };
    return str.replace(/ş|Ş|ı|İ|ğ|Ğ|ü|Ü|ö|Ö|ç|Ç/g, function(match) {
        return turkishMap[match];
    });
}

startButton.addEventListener("click", function() {
    var player1Name = replaceTurkishCharacters(document.getElementById("player1Name").value.substring(0, 8));
    var player2Name = replaceTurkishCharacters(document.getElementById("player2Name").value.substring(0, 8));
    var player3Name = replaceTurkishCharacters(document.getElementById("player3Name").value.substring(0, 8));
    var player4Name = replaceTurkishCharacters(document.getElementById("player4Name").value.substring(0, 8));    
    playerNames.push(player1Name);
    playerNames.push(player2Name);
    playerNames.push(player3Name);
    playerNames.push(player4Name);
    MAX_SCORE = document.getElementById("maxScore").value;
    gameMode = document.getElementById("gameMode").value;
    
    showBracket();
});

startTournament.addEventListener("click", function() {
    document.getElementById('show-bracket').style.display = 'none';
    showCanvas();
});
}