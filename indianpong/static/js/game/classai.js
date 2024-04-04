
class PongGame {
    constructor() {
        this.canvas = document.getElementById('pongCanvas');
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 800;
        this.canvas.height = 600;
        // ... initialize other variables
        this.w = window;
        this.requestAnimationFrame =
          this.w.requestAnimationFrame ||
          this.w.webkitRequestAnimationFrame ||
          this.w.msRequestAnimationFrame ||
          this.w.mozRequestAnimationFrame;
    }

    init() {
        // ... initialize canvas, abilities, sounds, etc
        this.canvasContainer = document.querySelector('.ai-game');
        this.username = document.querySelector('.container-top').dataset.username;
        this.ainame = document.querySelector('.container-top').dataset.ainame;
        this.paddleColor = document.querySelector('.container-top').dataset.paddlecolor;
        this.playgroundColor = document.querySelector('.container-top').dataset.playgroundcolor;
        this.canvas.style.borderColor = playgroundColor; // Set the border color to the specified color

        // Pong Abilities
        this.giantMan = document.querySelector('.container-top').dataset.giantman;
        this.likeaCheater = document.querySelector('.container-top').dataset.likeacheater;
        this.fastandFurious = document.querySelector('.container-top').dataset.fastandfurious;
        this.rageofFire = document.querySelector('.container-top').dataset.rageoffire;
        this.frozenBall = document.querySelector('.container-top').dataset.frozenball;
        this.givemethemusic = document.querySelector('.container-top').dataset.givemethemthis.
        this.MUSIC_PATH = document.querySelector('.container-top').dataset.musicpath;

        this.gameMusic = false;
        this.defeatMusic = false;
        this.victoryMusic = false;
        this.victorySound = new Audio(MUSIC_PATH+ 'pong-victory-sound.mp3');
        this.defeatSound = new Audio(MUSIC_PATH+ 'pong-defeat-sound.mp3');
        this.gameSound = new Audio(MUSIC_PATH+ 'pong-music.mp3');
        this.lpaddleSound = new Audio(MUSIC_PATH+ 'one_beep_2_left.mp3');
        this.rpaddleSound = new Audio(MUSIC_PATH+ 'one_beep_2_right.mp3');
        this.wallSound = new Audio(MUSIC_PATH+ 'one_beep.mp3');

        /* Skill sounds */
        this.fastandFuriousSound = new Audio(MUSIC_PATH+ 'fast-and-furious.mp3');
        this.frozenBallSound = new Audio(MUSIC_PATH+ 'frozen-ball.mp3');
        /* gameSound.volume = 0.07; */
        /* Cordinates of the canvas */
        this.textWidth1 = ctx.measureText(username + ": " + score1).width;
        this.textWidth2 = ctx.measureText(ainame + ": " + score2).width;

        this.usernameX = 10;
        this.usernameY = 20;
        this.start_time;
        // ainame metni sağ üst köşede
        this.ainameX = canvas.width - textWidth2 - 10;
        this.ainameY = 20;

        // if giantMan abilities equiped
        this.abilities_paddleHeight = (giantMan == "true") ? 115 : 100;
        this.paddleWidth = 10;
        this.paddleHeight = 100;
        this.paddleSpeed = 15;
        this.paddleY = (canvas.height - paddleHeight) / 2;
        this.paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};
        this.paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: abilities_paddleHeight, dy: paddleSpeed};

        // Ball object
        this.ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10, speed: 5, dx: 1, dy: 1};

        // Scores
        this.score1 = 0;
        this.score2 = 0;

        this.MAX_SCORE = 3;

        // Player Abilities
        this.likeaCheaterCount = 0;
        this.fastandFuriousCount = 0;
        this.frozenBallCount = 0;
        this.aiFrozenBallCount = 0;
        this.aiLikeaCheaterCount = 0;
        this.aiFastandFuriousCount = 0;

        this.isFrozenBallActive = false;

        // Add a new variable to track if the game is paused
        this.isScored = false;
        this.gameScreen = false;
        this.gameStarted = false;
        this.isPaused = false;
        this.upPressed = false;
        this.downPressed = false;
        this.upPressedAI = false;
        this.firstMove = false;
        this.downPressedAI = false;
        // Add a new variable for AI's target position
        this.moveThreshold = 8;
        this.targetY = paddle2.y;


        this.volumeSlider = document.getElementById('volumeSlider');
        this.volumeIcon = document.getElementById('volumeIcon');
        this.volumeControl = document.getElementById('volumeControl');

        this.volumeSlider.addEventListener('input', function() {
            this.volume = parseFloat(this.volumeSlider.value);
            this.setVolume(this.volume);

            if (this.volume === 0) {
                // Eğer ses sıfırsa, ikonu mute icon olarak değiştir
                this.volumeIcon.classList.remove('bi-volume-up-fill');
                this.volumeIcon.classList.add('bi-volume-mute-fill');
            } else {
                // Değilse, ikonu normal volume icon olarak değiştir
                this.volumeIcon.classList.remove('bi-volume-mute-fill');
                this.volumeIcon.classList.add('bi-volume-up-fill');
            }
        });

        this.w.addEventListener('load', function() {
            // Kaydedilmiş ses seviyesini kontrol et
            this.savedVolume = localStorage.getItem('savedVolume');
            this.savedSlider = localStorage.getItem('savedSlider');
            if (this.savedVolume !== null) {
                // Kaydedilmiş ses seviyesi varsa, slider'ı ve ses seviyesini ayarla
                this.volumeSlider.value = this.savedSlider;
                this.setVolume(this.savedVolume);
                // İkona göre ses simgesini ayarla
                if (this.savedVolume == 0) {
                    this.volumeIcon.classList.remove('bi-volume-up-fill');
                    this.volumeIcon.classList.add('bi-volume-mute-fill');
                }
            }
        });
        
        // Ses simgesine tıklandığında
        this.volumeIcon.addEventListener('click', function() {
            // Ses kontrolünün görünürlüğünü değiştirme
            this.toggleVolumeIcon();
        });

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

        document.getElementById('restartButton').addEventListener('click', restartGame);
        document.getElementById('exitButton').addEventListener('click', exitGame);

        this.modal = document.getElementById('exampleModalGame');

        // Modal açılma olayını dinle
        this.modal.addEventListener('show.bs.modal', function (event) {
            // Oyunu duraklat
            this.isPaused = true;
        });

        // Modal kapatılma olayını dinle
        this.modal.addEventListener('hide.bs.modal', function (event) {
            // Oyunu devam ettir
            this.isPaused = false;
        });
    }

    // Update the ball and paddle positions, handle collisions, etc.
    update() {
        // If the game is paused, don't update anything
        if (this.isPaused) return;
        ball.x += ball.speed * ball.dx;
        ball.y += ball.speed * ball.dy;
        

        // Check for collisions with paddles
        if (ball.y + ball.radius >= paddle1.y && ball.y - ball.radius <= paddle1.y + paddle1.height && ball.dx < 0) {       
            if (ball.x - ball.radius <= paddle1.x + paddle1.width) {
                // Çarpışma var, topun x koordinatını paddle'ın yanına ayarla ve yönünü tersine çevir
                startLPaddleSound();
                if (rageofFire == "true") {
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
        else if (ball.y + ball.radius >= paddle2.y && ball.y - ball.radius <= paddle2.y + paddle2.height && ball.dx > 0) {
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
        if (this.score1 == this.MAX_SCORE || this.score2 == this.MAX_SCORE && this.gameScreen == false) {
            this.gameScreen = true;
            if (this.score1 == this.MAX_SCORE) {   
                this.sendWinnerToBackend(this.username, "IndianAI", this.score1, this.score2, this.start_time);
            } else {
                this.sendWinnerToBackend("IndianAI", this.username, this.score2, this.score1, this.start_time);
            }   
            this.showGameOverScreen();
            
        }

        // Move the paddles
        if (this.upPressed && this.paddle1.y > 0 && !this.isScored) {
            this.paddle1.y -= this.paddle1.dy;
        } else if (this.downPressed && this.paddle1.y < this.canvas.height - this.paddle1.height && !this.isScored) {
            this.paddle1.y += this.paddle1.dy;
        }

        // Move the AI paddle towards the target position
        if (this.targetY < this.paddle2.y - this.moveThreshold && this.paddle2.y > 0 && !this.isScored) {
            this.paddle2.y -= this.paddle2.dy;
        } else if (this.targetY > this.paddle2.y + this.moveThreshold && this.paddle2.y < this.canvas.height - this.paddle2.height && !this.isScored) {
            this.paddle2.y += this.paddle2.dy;
        }

        // Prevent the paddles from moving off the canvas
        if (this.paddle1.y < 0) {
            this.paddle1.y = 0;
        } else if (this.paddle1.y > this.canvas.height - this.paddle1.height) {
            this.paddle1.y = this.canvas.height - this.paddle1.height;
        }
        if (this.paddle2.y < 0) {
            this.paddle2.y = 0;
        } else if (this.paddle2.y > this.canvas.height - this.paddle2.height) {
            this.paddle2.y = this.canvas.height - this.paddle2.height;
        }
    }

    // ... draw the game elements on the canvas
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Create a radial gradient for the background
        var gradient = this.ctx.createRadialGradient(this.canvas.width / 2, this.canvas.height / 2, 10, this.canvas.width / 2, this.canvas.height / 2, 300);
        gradient.addColorStop(0, 'lightgrey');
        gradient.addColorStop(1, 'darkgrey');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
        // Draw the middle dotted line
        this.ctx.beginPath();
        this.ctx.setLineDash([5, 15]);
        this.ctx.moveTo(this.canvas.width / 2, 0);
        this.ctx.lineTo(this.canvas.width / 2, this.canvas.height);
        this.ctx.strokeStyle = "black";
        this.ctx.stroke();

        // Draw the middle dotted circle
        this.ctx.beginPath();
        this.ctx.arc(this.canvas.width / 2, this.canvas.height / 2, 50, 0, Math.PI * 2, false);
        this.ctx.setLineDash([5, 15]);
        this.ctx.stroke();
    
        
        // Add shadow to the paddles
        this.ctx.shadowColor = 'black';
        this.ctx.shadowBlur = 10;
        this.ctx.shadowOffsetX = 5;
        this.ctx.shadowOffsetY = 5;
        
        
        this.ctx.fillStyle = this.paddleColor
        this.ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
        // If paddle2 is on the right, draw the shadow to the left
        this.ctx.shadowOffsetX = -5;
        this.ctx.shadowOffsetY = 5;
        this.ctx.fillRect(this.paddle2.x, this.paddle2.y, this.paddle2.width, this.paddle2.height);
        
        // Add shiny effect to the ball
        this.ctx.beginPath();
        this.ctx.arc(this.ball.x, this.ball.y, this.ball.radius, 0, Math.PI*2, false);
        var gradient = this.ctx.createRadialGradient(this.ball.x, this.ball.y, 0, this.ball.x, this.ball.y, this.ball.radius);
        gradient.addColorStop(0, 'white');
        gradient.addColorStop(0.1, 'gold');
        gradient.addColorStop(1, 'darkorange');
        this.ctx.fillStyle = gradient;
        this.ctx.fill();
        this.ctx.closePath();
    
        // Reset shadow properties
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
    
        this.ctx.font = "16px Roboto";
        this.ctx.fillStyle = 'white';
        this.ctx.fillText(this.username + ": " + this.score1, this.usernameX, this.usernameY);
        this.ctx.fillText(this.ainame + ": " + this.score2, this.ainameX, this.ainameY);
    }


    // ... start the game loop
    startGame() {
        // The main game loop
        var main = function () {
            if (this.gameMusic === false && this.givemethemusic == "true") {
                this.startBackgroundMusic();
            }
            if (!this.start_time)
                this.start_time = new Date();
            // Request to do this again ASAP
            if (!this.isPaused && this.gameScreen == false) {
                this.update();
                this.render();
            }

            this.requestAnimationFrame(main);
        };
    }

    // ... implement the AI logic
    aiPlayer() {
        // Ai Player
        let reactionDelaySlider = document.getElementById('reactionDelay');
        let delayValueSpan = document.getElementById('delayValue');
        // Update the reactionDelay variable whenever the slider value changes
        reactionDelaySlider.oninput = function() {
            // Delay in milliseconds
            reactionDelay = reactionDelaySlider.value / this.ball.speed;
            delayValueSpan.innerText = Math.round(reactionDelay); // Display the current value of the slider
            reactionDelaySlider.value = (this.value-this.min)/(this.max-this.min)*100
            /* this.style.background = 'linear-gradient(to right, violet, yellow ' + value + '%, #ccc ' + value + '%, #ccc)'; */
        }
        let reactionDelay = Math.round(reactionDelaySlider.value / this.ball.speed);
        let lastBallPosition = { x: this.ball.x, y: this.ball.y };
        let ballDirection = { x: 0, y: 0 };
        let predictedY = this.paddle2.y;

        // AI's logic
        setInterval(() => {
            // Skills
            if (this.frozenBall == "true" && this.aiFrozenBallCount < 1) {
                // Kontrol edilecek koşul: Top köşeye gidiyorsa ve AI da ters köşede ise
                if (this.ball.dx > 0 && this.ball.x > this.canvas.width / 2 && this.ball.y > this.canvas.height / 2) {
                    // AI'nın kendisi için kullanması için bir kontrol ekleyin
                    if (this.ball.x > this.paddle2.x + this.paddle2.width) {
                        this.frozenBallAbility();
                        this.aiFrozenBallCount += 1;
                    }
                }
            }
            if (this.fastandFurious == "true" && this.aiFastandFuriousCount < 1 && this.isFrozenBallActive == false) {
                // Top rakip yarı sahaya doğru gidiyorsa ve topun X koordinatı AI'nın ceza sahasında ise
                if (this.ball.dx < 0 && this.ball.x > this.canvas.width / 2 && this.ball.x < this.canvas.width - this.paddle2.width && this.ball.speed > 5) {
                    //console.log("AI Fast and Furious yeteneğini kullandı ve değerleri şu şekilde: ", ball.speed);
                    this.fastandFuriousAbility();
                    this.aiFastandFuriousCount += 1;
                }
            }
            

            if (this.likeaCheater == "true" && this.aiLikeaCheaterCount < 1) {
                if (this.score2 < this.score1 || this.score1 === this.MAX_SCORE - 1 || this.score2 + 1 === this.MAX_SCORE) {
                    // console.log("AI Like a Cheater yeteneğini kullandı ve değerleri şu şekilde: ", score1, score2);
                    this.likeaCheaterAbility(true);
                    this.aiLikeaCheaterCount += 1;
                }
            }

            // Calculate ball direction
            ballDirection.x = this.ball.x - lastBallPosition.x;
            ballDirection.y = this.ball.y - lastBallPosition.y;

            // Predict ball's y position when it reaches the paddle
            let timeToReachPaddle = (this.paddle2.x - this.ball.x) / ballDirection.x;
            predictedY = this.ball.y + ballDirection.y * timeToReachPaddle;

            // Clamp prediction within canvas
            predictedY = Math.max(0, Math.min(this.canvas.height, predictedY));
            
            // Update last ball position
            lastBallPosition = { x: this.ball.x, y: this.ball.y };

            // Update AI paddle movement variables based on predicted position
            this.upPressedAI = predictedY < this.paddle2.y;
            this.downPressedAI = predictedY > this.paddle2.y;

            targetY = predictedY - this.paddle2.height / 2;
        }, reactionDelay);
    }

    // ... reset the ball position
    resetBall() {
        this.isScored = true;
        this.isPaused = true;
        this.ball.speed = 5;
        this.paddleSpeed = 15;
        this.ball.dx = -this.ball.dx;
        this.ball.dy = -this.ball.dy;
        setTimeout(() => {     
            this.ball.x = this.canvas.width / 2;
            this.ball.y = this.canvas.height / 2;
            this.isPaused = false;
            this.isScored = false;
        }, 500);
    }

    frozenBallAbility() {
        var nowBallSpeed = this.ball.speed;
        this.isFrozenBallActive = true;
        this.startfrozenBallSound();
        this.ball.speed = 0;
        setTimeout(function() {
            this.ball.speed = nowBallSpeed;
            this.isFrozenBallActive = false;
        }, 1500);
    }
    
    likeaCheaterAbility(isAi) {
        if (isAi === true) {
            this.score2++;
            if (this.score1 > 0) {
                this.score1--;
            }
        }
        else {
            this.score1++;
            if (this.score2 > 0) {
                this.score2--;
            }
        }
    }
    
    fastandFuriousAbility() {
        this.startfastandFuriousSound();
        this.ball.speed += 10;
    }

    // ... reset the paddle positions
    resetPaddles() {
        this.paddle1.y = (this.canvas.height - this.abilities_paddleHeight) / 2; 
        this.paddle2.y = (this.canvas.height - this.abilities_paddleHeight) / 2;
    }

    // ... reset the abilities
    resetAbilities() {
        this.likeaCheaterCount = 0;
        this.fastandFuriousCount = 0;
        this.frozenBallCount = 0;
        this.aiFrozenBallCount = 0;
        this.aiLikeaCheaterCount = 0;
        this.aiFastandFuriousCount = 0;
    }

    // ... reset the game state
    resetGame() {
        this.start_time = null;
        this.gameScreen = false;
        this.score1 = 0;
        this.score2 = 0;
        this.resetBall();
        this.resetPaddles();
        this.resetAbilities();
    }

    // Stop the background music
    stopBackgroundMusic() {
        setTimeout(function() {
            if (this.gameSound) {
                this.gameSound.pause();
            }
        }, 1000);    
    }

    startBackgroundMusic() {
        setTimeout(function() {
            if (vgameSound) {
                this.gameSound.loop = true;
                this.gameSound.play();
            }
        }, 1000);
        this.gameMusic = true;
    }

    // Play the result sound
    playResultSound(isVictory) {
        //stopBackgroundMusic(); // Önce müziği durdur
        if (isVictory) {  
            setTimeout(function() {
                /* victorySound.volume = 0.2; */  
                this.victorySound.play();
            }, 50);
            this.victoryMusic = true;
        } else {
            setTimeout(function() {
                /* defeatSound.volume = 0.2;  */ 
                this.defeatSound.play();
            }, 50);
            this.defeatMusic = true;
        }
    }

    startLPaddleSound() {
        setTimeout(function() {  
            this.lpaddleSound.play();
        }, 50);
    }

    startRPaddleSound() {
        setTimeout(function() {  
            this.rpaddleSound.play();
        }, 50);
    }

    startWallSound() {
        setTimeout(function() {  
            this.this.wallSound.play();
        }, 50);
    }

    // Skill Sounds

    startfastandFuriousSound() {
        setTimeout(function() {  
            /* fastandFuriousSound.volume = 0.2; */
            this.fastandFuriousSound.play();
        }, 50);
    }

    startfrozenBallSound() {
        setTimeout(function() {  
            //frozenBallSound.volume = 0.2;
            this.frozenBallSound.play();
        }, 50);
    }

    setVolume(volume) {
        // Ses seviyesini ayarla
        this.victorySound.volume = volume;
        this.defeatSound.volume = volume;
        this.gameSound.volume = volume;
        this.lpaddleSound.volume = volume;
        this.rpaddleSound.volume = volume;
        this.wallSound.volume = volume;
        this.fastandFuriousSound.volume = volume;
        this.frozenBallSound.volume = volume;
    
        // Kaydet
        this.localStorage.setItem('savedVolume', volume);
        this.localStorage.setItem('savedSlider', this.volumeSlider.value);
    }

    toggleVolumeIcon() {
        if (this.volumeIcon.classList.contains('bi-volume-up-fill')) {
            this.volumeIcon.classList.remove('bi-volume-up-fill');
            this.volumeIcon.classList.add('bi-volume-mute-fill');
            // Ses seviyesini sıfıra ayarla
            this.setVolume(0);
        } else {
            this.volumeIcon.classList.remove('bi-volume-mute-fill');
            this.volumeIcon.classList.add('bi-volume-up-fill');
            // Kaydedilmiş ses seviyesini geri yükle
            var volume = parseFloat(volumeSlider.value);
            this.setVolume(volume);
        }
    }

    getOutcomeMessage(selectedLanguage, outcome) {
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

    // ... show the game over screen
    showGameOverScreen() {
   
        var winnerText = (this.score1 == this.MAX_SCORE) ? this.getOutcomeMessage(selectedLanguage, "win") : "";
        var loserText = (score2 == MAX_SCORE) ? this.getOutcomeMessage(selectedLanguage, "lose") : "";
        if (this.score1 == this.MAX_SCORE) {
            playResultSound(true); // Zafer durumu
        } else {
            playResultSound(false); // Yenilgi durumu
        }
        document.getElementById('winnerText').innerText = winnerText;
        document.getElementById('loserText').innerText = loserText;
        document.getElementById('gameOverScreen').style.display = 'block';
    }

    // ... restart the game
    restartGame() {
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

    // ... exit the game
    exitGame() {
        window.location.href = '/pong-game-find';  // ?
    }

    // ... send the winner data to the backend
    sendWinnerToBackend(winner, loser, winnerscore, loserscore, start_time) {
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
}

// Usage:
const game = new PongGame();
game.init();
game.startGame();
