
const canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;


const canvasContainer = document.querySelector('.ai-game');
const username = document.querySelector('.container-top').dataset.username;
const ainame = document.querySelector('.container-top').dataset.ainame;
const paddleColor = document.querySelector('.container-top').dataset.paddlecolor;
const playgroundColor = document.querySelector('.container-top').dataset.playgroundcolor;
canvas.style.borderColor = playgroundColor; // Set the border color to the specified color

// Pong Abilities
const giantMan = document.querySelector('.container-top').dataset.giantman;
const likeaCheater = document.querySelector('.container-top').dataset.likeacheater;
const fastandFurious = document.querySelector('.container-top').dataset.fastandfurious;
const rageofFire = document.querySelector('.container-top').dataset.rageoffire;
const frozenBall = document.querySelector('.container-top').dataset.frozenball;
const givemethemusic = document.querySelector('.container-top').dataset.givemethemusic;

const MUSIC_PATH = document.querySelector('.container-top').dataset.musicpath;

var gameMusic = false;
var defeatMusic = false;
var victoryMusic = false;
var victorySound = new Audio(MUSIC_PATH+ 'pong-victory-sound.mp3');
var defeatSound = new Audio(MUSIC_PATH+ 'pong-defeat-sound.mp3');
var gameSound = new Audio(MUSIC_PATH+ 'pong-music.mp3');
var lpaddleSound = new Audio(MUSIC_PATH+ 'one_beep_2_left.mp3');
var rpaddleSound = new Audio(MUSIC_PATH+ 'one_beep_2_right.mp3');
var wallSound = new Audio(MUSIC_PATH+ 'one_beep.mp3');

/* Skill sounds */
var fastandFuriousSound = new Audio(MUSIC_PATH+ 'fast-and-furious.mp3');
var frozenBallSound = new Audio(MUSIC_PATH+ 'frozen-ball.mp3');

/* gameSound.volume = 0.07; */
/* Cordinates of the canvas */
var textWidth1 = ctx.measureText(username + ": " + score1).width;
var textWidth2 = ctx.measureText(ainame + ": " + score2).width;

var usernameX = 10;
var usernameY = 20;
var start_time;
// ainame metni sağ üst köşede
var ainameX = canvas.width - textWidth2 - 10;
var ainameY = 20;

// if giantMan abilities equiped
var abilities_paddleHeight = (giantMan == "true") ? 120 : 100;
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
var aiFrozenBallCount = 0;
var aiLikeaCheaterCount = 0;
var aiFastandFuriousCount = 0;

var isFrozenBallActive = false;

// Add a new variable to track if the game is paused
let isScored = false;
var gameScreen = false;
var gameStarted = false;
var isPaused = false;
let upPressed = false;
let downPressed = false;
let upPressedAI = false;
let firstMove = false;
let downPressedAI = false;
// Add a new variable for AI's target position
let moveThreshold = 8;
let targetY = paddle2.y;

function resetAbilities() {
    likeaCheaterCount = 0;
    fastandFuriousCount = 0;
    frozenBallCount = 0;
    aiFrozenBallCount = 0;
    aiLikeaCheaterCount = 0;
    aiFastandFuriousCount = 0;
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
            // Çarpışma var, topun x koordinatını paddle'ın yanına ayarla ve yönünü tersine çevir
            startLPaddleSound();
            if (rageofFire == "true") {
                if (Math.random() <= 0.5) {
                    ball.speed += 1;
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
            startRPaddleSound();
            // Çarpışma var, topun x koordinatını paddle'ın yanına ayarla ve yönünü tersine çevir
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
        startWallSound();
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
    if (score1 == MAX_SCORE || score2 == MAX_SCORE && gameScreen == false) {
        gameScreen = true;
        if (score1 == MAX_SCORE) {   
            sendWinnerToBackend(username, "IndianAI", score1, score2, start_time);
        } else {
            sendWinnerToBackend("IndianAI", username, score2, score1, start_time);
        }   
        showGameOverScreen();
        
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
    ctx.fillText(username + ": " + score1, usernameX, usernameY);
    ctx.fillText(ainame + ": " + score2, ainameX, ainameY);
}


// The main game loop
var main = function () {
    if (gameMusic === false && givemethemusic == "true") {
        startBackgroundMusic();
    }
    if (!start_time)
        start_time = new Date();
    // Request to do this again ASAP
    if (!isPaused && gameScreen == false) {
        update();
        render();
    }


    requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
function startGame() {
    main();
}
// Stop the background music
function stopBackgroundMusic() {
    setTimeout(function() {
        if (gameSound) {
            gameSound.pause();
        }
    }, 1000);    
}

function startBackgroundMusic() {
    setTimeout(function() {
        if (gameSound) {
            gameSound.loop = true;
            gameSound.play();
        }
    }, 1000);
    gameMusic = true;
}

// Play the result sound
function playResultSound(isVictory) {
    //stopBackgroundMusic(); // Önce müziği durdur
    if (isVictory) {  
        setTimeout(function() {
            /* victorySound.volume = 0.2; */  
            victorySound.play();
        }, 50);
        victoryMusic = true;
    } else {
        setTimeout(function() {
            /* defeatSound.volume = 0.2;  */ 
            defeatSound.play();
        }, 50);
        defeatMusic = true;
    }
}

function startLPaddleSound() {
    setTimeout(function() {  
        lpaddleSound.play();
    }, 50);
}

function startRPaddleSound() {
    setTimeout(function() {  
        rpaddleSound.play();
    }, 50);
}

function startWallSound() {
    setTimeout(function() {  
        wallSound.play();
    }, 50);
}

// Skill Sounds

function startfastandFuriousSound() {
    setTimeout(function() {  
        /* fastandFuriousSound.volume = 0.2; */
        fastandFuriousSound.play();
    }, 50);
}

function startfrozenBallSound() {
    setTimeout(function() {  
        //frozenBallSound.volume = 0.2;
        frozenBallSound.play();
    }, 50);
}

//Music volume control

const volumeSlider = document.getElementById('volumeSlider');

volumeSlider.addEventListener('input', function() {
    const volume = parseFloat(volumeSlider.value);
    setVolume(volume);

    if (volume === 0) {
        // Eğer ses sıfırsa, ikonu mute icon olarak değiştir
        volumeIcon.classList.remove('bi-volume-up-fill');
        volumeIcon.classList.add('bi-volume-mute-fill');
    } else {
        // Değilse, ikonu normal volume icon olarak değiştir
        volumeIcon.classList.remove('bi-volume-mute-fill');
        volumeIcon.classList.add('bi-volume-up-fill');
    }
});

function setVolume(volume) {
    // Ses seviyesini ayarla
    victorySound.volume = volume;
    defeatSound.volume = volume;
    gameSound.volume = volume;
    lpaddleSound.volume = volume;
    rpaddleSound.volume = volume;
    wallSound.volume = volume;
    fastandFuriousSound.volume = volume;
    frozenBallSound.volume = volume;

    // Kaydet
    localStorage.setItem('savedVolume', volume);
    localStorage.setItem('savedSlider', volumeSlider.value);
}
// Sayfa yüklendiğinde
window.addEventListener('load', function() {
    // Kaydedilmiş ses seviyesini kontrol et
    const savedVolume = localStorage.getItem('savedVolume');
    const savedSlider = localStorage.getItem('savedSlider');
    if (savedVolume !== null) {
        // Kaydedilmiş ses seviyesi varsa, slider'ı ve ses seviyesini ayarla
        volumeSlider.value = savedSlider;
        setVolume(savedVolume);
        // İkona göre ses simgesini ayarla
        if (savedVolume == 0) {
            volumeIcon.classList.remove('bi-volume-up-fill');
            volumeIcon.classList.add('bi-volume-mute-fill');
        }
    }
});

const volumeIcon = document.getElementById('volumeIcon');
const volumeControl = document.getElementById('volumeControl');

// Ses simgesine tıklandığında
volumeIcon.addEventListener('click', function() {
    // Ses kontrolünün görünürlüğünü değiştirme
    toggleVolumeIcon();
});

function toggleVolumeIcon() {
    if (volumeIcon.classList.contains('bi-volume-up-fill')) {
        volumeIcon.classList.remove('bi-volume-up-fill');
        volumeIcon.classList.add('bi-volume-mute-fill');
        // Ses seviyesini sıfıra ayarla
        setVolume(0);
    } else {
        volumeIcon.classList.remove('bi-volume-mute-fill');
        volumeIcon.classList.add('bi-volume-up-fill');
        // Kaydedilmiş ses seviyesini geri yükle
        const volume = parseFloat(volumeSlider.value);
        setVolume(volume);
    }
}


// Reset the ball to the center
function resetBall() {
    isScored = true;
    isPaused = true;
    ball.speed = 5;
    paddleSpeed = 15;
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
    startfrozenBallSound();
    ball.speed = 0;
    setTimeout(function() {
        ball.speed = nowBallSpeed;
        isFrozenBallActive = false;
    }, 1500);
}

function likeaCheaterAbility(isAi) {
    if (isAi === true) {
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
    startfastandFuriousSound();
    ball.speed += 10;
}

// Control paddle1 with w, s keys
document.addEventListener("keydown", function(event) {
    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
        upPressed = true;
    } 
    else if (event.key === "s" || event.key === "S" || event.key === "ArrowDown") {
        downPressed = true;
    }
    else if (event.key === '1' && likeaCheaterCount < 1 && likeaCheater == "true") {
        likeaCheaterAbility(false);
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
    if (event.code === 'Space' && gameStarted === false) { // Boşluk tuşu kodu
        gameStarted = true;
        startGameCountdown(); // Oyunu başlatmak için geri sayım başlat
    }
});

document.addEventListener("keyup", function(event) {
    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
        upPressed = false;
    } else if (event.key === "s" || event.key === "S" || event.key === "ArrowDown") {
        downPressed = false;
    }
});


// Ai Player
let reactionDelaySlider = document.getElementById('reactionDelay');
let delayValueSpan = document.getElementById('delayValue');
// Update the reactionDelay variable whenever the slider value changes
reactionDelaySlider.oninput = function() {
    // Delay in milliseconds
    reactionDelay = this.value / ball.speed;
    delayValueSpan.innerText = Math.round(reactionDelay); // Display the current value of the slider
    let value = (this.value-this.min)/(this.max-this.min)*100
    this.style.background = 'linear-gradient(to right, violet, yellow ' + value + '%, #ccc ' + value + '%, #ccc)';
}
let reactionDelay = Math.round(reactionDelaySlider.value / ball.speed);
let lastBallPosition = { x: ball.x, y: ball.y };
let ballDirection = { x: 0, y: 0 };
let predictedY = paddle2.y;

// AI's logic
setInterval(() => {
    // Skills
    if (frozenBall == "true" && aiFrozenBallCount < 1) {
        // Kontrol edilecek koşul: Top köşeye gidiyorsa ve AI da ters köşede ise
        if (ball.dx > 0 && ball.x > canvas.width / 2 && ball.y > canvas.height / 2) {
            // AI'nın kendisi için kullanması için bir kontrol ekleyin
            if (ball.x > paddle2.x + paddle2.width) {
                frozenBallAbility();
                aiFrozenBallCount += 1;
            }
        }
    }
    if (fastandFurious == "true" && aiFastandFuriousCount < 1 && isFrozenBallActive == false) {
        // Top rakip yarı sahaya doğru gidiyorsa ve topun X koordinatı AI'nın ceza sahasında ise
        if (ball.dx < 0 && ball.x > canvas.width / 2 && ball.x < canvas.width - paddle2.width && ball.speed > 5) {
            //console.log("AI Fast and Furious yeteneğini kullandı ve değerleri şu şekilde: ", ball.speed);
            fastandFuriousAbility();
            aiFastandFuriousCount += 1;
        }
    }
    

    if (likeaCheater == "true" && aiLikeaCheaterCount < 1) {
        if (score2 < score1 || score1 === MAX_SCORE - 1 || score2 + 1 === MAX_SCORE) {
            // console.log("AI Like a Cheater yeteneğini kullandı ve değerleri şu şekilde: ", score1, score2);
            likeaCheaterAbility(true);
            aiLikeaCheaterCount += 1;
        }
    }

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

// Reset the paddle1 position?
function resetPaddles() {
    paddle1.y = (canvas.height - abilities_paddleHeight) / 2; 
    paddle2.y = (canvas.height - abilities_paddleHeight) / 2;
}

function startGameCountdown() {
    // Geri sayım ekranını göster
    // Örnek olarak bir HTML elementi üzerine yazıyorum, siz kendi tasarımınıza göre ayarlayabilirsiniz
    var countdown = document.getElementById('countdownTimer');
    var countdownElement = document.getElementById('countdown');
    // 3 saniye sonra
    setTimeout(function() {
        countdown.textContent = '3';
    }, 50);

    // 2 saniye sonra
    setTimeout(function() {
        countdown.textContent = '2';
    }, 1050);

    // 1 saniye sonra
    setTimeout(function() {
        countdown.textContent = '1';
    }, 2050);

    // Oyunu başlat
    setTimeout(function() {
        countdownElement.style.display = 'none'; // Geri sayım elementini kaldır
        startGame(); // Oyunu başlatan fonksiyon
    }, 4000);
}

function resetGame() {
    start_time = null;
    gameScreen = false;
    score1 = 0;
    score2 = 0;
    resetBall();
    resetPaddles();
    resetAbilities();
}

function getOutcomeMessage(selectedLanguage, outcome) {
    // Dil çevirilerini içeren bir sözlük oluşturalım
    const translations = {
        'hi': {
            'win': 'आप जीत गए',
            'lose': 'आप हार गए'
        },
        'pt': {
            'win': 'Você ganhou',
            'lose': 'Você perdeu'
        },
        'en': {
            'win': 'YOU WIN',
            'lose': 'YOU LOSE'
        },
        'tr': {
            'win': 'KAZANDINIZ',
            'lose': 'KAYBETTINIZ'
        }
    };
    // Seçilen dil ve sonucu kullanarak uygun metni belirleyelim
    const message = translations[selectedLanguage] ? translations[selectedLanguage][outcome] : translations['en'][outcome];
    return message;
}

// Oyun bitiş ekranını gösteren fonksiyon
function showGameOverScreen() {
    //var winnerText = (score1 == MAX_SCORE) ? username + " wins!" : ainame + " wins!";
    
    var winnerText = (score1 == MAX_SCORE) ? getOutcomeMessage(selectedLanguage, "win") : "";
    var loserText = (score2 == MAX_SCORE) ? getOutcomeMessage(selectedLanguage, "lose") : "";
    if (score1 == MAX_SCORE) {
        playResultSound(true); // Zafer durumu
    } else {
        playResultSound(false); // Yenilgi durumu
    }
    document.getElementById('winnerText').innerText = winnerText;
    document.getElementById('loserText').innerText = loserText;
/*     if (score1 > score2) {
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(11, 22, 8, 0.8)';
    }
    else {
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(20, 5, 5, 0.8)';
    } */
    document.getElementById('gameOverScreen').style.display = 'block';
}

// Oyunu tekrar başlatan fonksiyon
function restartGame() {
    document.getElementById('gameOverScreen').style.display = 'none';
    resetGame();
    if (victoryMusic === true) {
        setTimeout(function() {  
            victorySound.pause();
            victorySound.currentTime = 0;
        }, 1000);
        victoryMusic = false;
    }
    if (defeatMusic === true) {
        setTimeout(function() {
            defeatSound.pause();
            defeatSound.currentTime = 0;
        }, 1000);
        defeatMusic = false;
    }
    if (givemethemusic === "true")
        startBackgroundMusic();
}

// Çıkış yapma işlemleri
function exitGame() {
    window.location.href = '/pong-game-find';
}

document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('exitButton').addEventListener('click', exitGame);

var modal = document.getElementById('exampleModalGame');

// Modal açılma olayını dinle
modal.addEventListener('show.bs.modal', function (event) {
    // Oyunu duraklat
    isPaused = true;
});

// Modal kapatılma olayını dinle
modal.addEventListener('hide.bs.modal', function (event) {
    // Oyunu devam ettir
    isPaused = false;
});

function sendWinnerToBackend(winner, loser, winnerscore, loserscore, start_time) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var finish_time = new Date();
    const data = {
        game: "pong",
        winner: winner,
        loser: loser,
        winnerscore: winnerscore,
        loserscore: loserscore,
        start_time: start_time,
        finish_time: finish_time
    };

    fetch('/update_winner', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        
    })
    .catch(error => {
        console.error('There was a problem updating the winner:', error);
    });
}