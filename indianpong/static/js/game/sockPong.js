export function RemotePong() {

const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
const lang = cookie ? cookie.split('=')[1] : 'en';
 
function showToast(content, status, iconClass) {
    const liveToast = document.getElementById('liveToast');
    var toastContent = document.querySelector('#liveToast .fw-semibold');
    var toastIcon = document.querySelector('.toast-body .i-class i');

    toastIcon.className = iconClass;
    liveToast.classList.remove('text-bg-danger'); 
    liveToast.className = 'toast'; 
    liveToast.classList.add(status);

    toastContent.textContent = content;
    const toast = new bootstrap.Toast(liveToast);
    toast.show();
    setTimeout(function() {
        toast.hide();
    }, 8000);
}    
    
    // Extract game_id and game_type from the URL
const pathArray = window.location.pathname.split('/');
const gameType = pathArray[2]; // Assuming game_type is the third segment of the URL
const gameId = pathArray[3]; // Assuming game_id is the fourth segment of the URL


// Connect to the WebSocket server using the extracted game_id and game_type
const matchsocket = new WebSocket(`ws://${window.location.host}/ws/remote-game/${gameType}/${gameId}/`); //? Maybe we need to pass game type and game id here


const canvas = document.getElementById('pongCanvas');
var ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;

const checkbox = document.getElementById('flexSwitchCheckDefault');
const selectedGameModeLabel = document.getElementById('selectedGameMode');

let gameMode = "Vanilla";

// Custom items
const leftArea = document.getElementById('left-area-display');
const paddleColor = document.querySelector('.left-card').dataset.paddlecolor;
const playgroundColor = document.querySelector('.left-card').dataset.playgroundcolor;
canvas.style.borderColor = playgroundColor;
const giantMan = document.querySelector('.left-card').dataset.giantman;
const likeaCheater = document.querySelector('.left-card').dataset.likeacheater;
const fastandFurious = document.querySelector('.left-card').dataset.fastandfurious;
const rageofFire = document.querySelector('.left-card').dataset.rageoffire;
const frozenBall = document.querySelector('.left-card').dataset.frozenball;
const tournament = document.querySelector('.left-card').dataset.tournament;

let likeaCheaterCount = 0;
let fastandFuriousCount = 0;
let frozenBallCount = 0;

let isFrozenBallActive = false;

// Paddle objects
var paddleWidth = 10;
var paddleHeight = 100;
var paddleY = (canvas.height - paddleHeight) / 2;
var paddle1 = {x: 0, y: paddleY, width: paddleWidth, height: paddleHeight};
var paddle2 = {x: canvas.width - paddleWidth, y: paddleY, width: paddleWidth, height: paddleHeight};

// Ball object
var ball = {x: canvas.width / 2, y: canvas.height / 2, radius: 10};

// maybe merge with my object
var player1 = {username: '', score: 0};
var player2 = {username: '', score: 0};

var my = {
    username: '', opponent_username: '', game_id: '', tournament_id: '', 
};

let upPressed = false;
let downPressed = false;

//Button
//const startButton = document.getElementById('startButton');
const leaveButton = document.getElementById('leaveButton');
leaveButton.style.display = 'none';
const gameOverScreen = document.getElementById('gameOverScreen');
const matchmakingButton = document.getElementById('matchmakingButton');
//const restartButton = document.getElementById('restartButton');
//startButton.style.display = 'none';
//restartButton.style.display = 'none';

// Envai
var textWidth1 = ctx.measureText(player1.username + ": " + player1.score).width;
var textWidth2 = ctx.measureText(player2.username + ": " + player2.score).width;

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
    
    ctx.fillStyle = paddleColor;
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

    ctx.font = "14px Roboto";
    ctx.fillStyle = 'white';
    ctx.fillText(player1.username + ": " + player1.score, 50, 20);
    ctx.fillText(player2.username + ": " + player2.score, canvas.width - textWidth2 - 80, 20);
}

var requestId;

// The main game loop
var startGame = function () {
    
    
    BallRequest();
    updatePaddlePosition();
    render();
    // Request to do this again ASAP
    requestId = requestAnimationFrame(startGame);
};

// When you want to stop the game loop
var stopGame = function() {
    cancelAnimationFrame(requestId);
};

function gameUtilsReset() {
    likeaCheaterCount = 0;
    fastandFuriousCount = 0;
    frozenBallCount = 0;
    isFrozenBallActive = false;

    if (giantMan == "true" && (gameMode === "Abilities" || tournament === "abilities"))
        sendAbility("giantMan");
    if (rageofFire == "true" && (gameMode === "Abilities" || tournament === "abilities"))
        sendAbility("rageofFire");
}

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame =
  w.requestAnimationFrame ||
  w.webkitRequestAnimationFrame ||
  w.msRequestAnimationFrame ||
  w.mozRequestAnimationFrame;

function paddleMove(player, y) {
    if (player === player1.username) {
        paddle1.y = y;
    } else if (player === player2.username) {
        paddle2.y = y;
    }
}

function ballMove(x, y) {
    ball.x = x;
    ball.y = y;
}

function scoreUpdate(player1_score, player2_score) {
    player1.score = player1_score;
    player2.score = player2_score;
}

matchsocket.onopen = function (e) {
    // Show some greeting message
    console.log('WebSocket connection established');
}

matchsocket.onclose = function (e) {
    //clearInterval(BallRequest);
    stopGame();
    console.error('WebSocket connection closed');
}

matchsocket.onerror = function (e) {
    console.error('Error: ' + e.data);
    //clearInterval(BallRequest);
    stopGame();
}

matchsocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    //console.log(data);
    switch (data.type) {
        case 'inlobby':
            // Self send message
            console.log('In lobby', data.user);
            if (my.username === '') {
                my.username = data.user;
            }
            // Take online users usernames and display them
            addUsersToTable(data.users);
            console.log('Online users', data.users);
            break;
            
        case 'user.inlobby':
            // Send others i joined the lobby
            console.log('User in lobby', data.user);
            // Add user to online users list
            if (data.user !== my.username) {
                addUsersToTable([data.user]);
            }
            if (lang === 'tr')
                showToast(data.user + ' katıldı!', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (lang === 'hi')  
                showToast(data.user + ' शामिल हो गया!', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (lang === 'pt')  
                showToast(data.user + ' entrou!', 'text-bg-success', 'bi bi-check-circle-fill')
            else
                showToast(data.user + ' joined!', 'text-bg-success', 'bi bi-check-circle-fill')
        break;

        case 'user.outlobby':
            // Send others user left the lobby
            console.log('User out lobby', data.user);
            // Remove user from online users list
            removeUserFromTable(data.user);
            if (lang === 'tr')
                showToast(data.user + ' ayrıldı!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (lang === 'hi')
                showToast(data.user + ' चला गया!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (lang === 'pt')
                showToast(data.user + ' saiu!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else
                showToast(data.user + ' left!', 'text-bg-danger', 'bi bi-check-circle-fill')
            break;

        case 'game.disconnected':
            //clearInterval(BallRequest);
            stopGame();
            gameOverScreen.style.display = 'block';
            showToast(`${data.disconnected} disconnected You are automatically winner`, 'text-bg-danger', 'bi bi-check-circle-fill')
            console.log('Player disconnected', data.disconnected);
            
        case 'game.invite':
            // Tell user that he/she is invited to a game
            console.log('Game invite', data.inviter);
            console.log('data: ', data.invitee + " " + my.username)
            // Display the modal for accepting or declining the invitation

            hideInviteButtons(data.inviter, data.invitee);
            
            const acceptButton = document.getElementById(`acceptButton${data.inviter}`);
            const declineButton = document.getElementById(`declineButton${data.inviter}`);
            if (data.invitee === my.username)  {
                if (lang === 'tr')
                    showToast(`${data.inviter} tarafından bir oyun daveti aldınız`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'hi')
                    showToast(`${data.inviter} द्वारा आपको एक खेल आमंत्रण मिला है`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'pt')
                    showToast(`Você recebeu um convite de jogo de ${data.inviter}`, 'text-bg-success', 'bi bi-check-circle-fill');
                else
                    showToast(`You received a game invitation from ${data.inviter}`, 'text-bg-success', 'bi bi-check-circle-fill')
                acceptButton.style.display = 'flex';
                declineButton.style.display = 'flex';
            }

            acceptButton.onclick = function () {
                accept(data.inviter);
                acceptButton.style.display = 'none';
                declineButton.style.display = 'none';
            };

            declineButton.onclick = function () {
                decline(data.inviter);
                acceptButton.style.display = 'none';
                declineButton.style.display = 'none';
            };

            console.log(`Invited Group: ${data.inviter} vs ${data.invitee}`);
            break;

        case 'tournament.match':
            checkbox.disabled = true;
            leftArea.style.display = 'none';
            player1.username = data.player1;
            player2.username = data.player2;
            my.game_id = data.game_id;
            my.tournament_id = data.tournament_id;
            leftArea.style.display = 'none';
            if (lang === 'tr')
                showToast(`Turnuva maçı başladı! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'hi')
                showToast(`टूर्नामेंट मैच शुरू हो गया! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'pt')
                showToast(`Jogo de torneio começou! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else
                showToast(`Tournament match started! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');

            render();
            showToast('Press Space to start the game', 'text-bg-primary', 'bi bi-exclamation-triangle-fill')

            document.addEventListener("keydown", SpaceKeyDown);

            console.log(`Tournament Id: ${data.tournament_id}, Match Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;

        case 'chat.game':
            checkbox.disabled = true;
            leftArea.style.display = 'none';
            player1.username = data.player1;
            player2.username = data.player2;
            my.game_id = data.game_id;
            my.opponent_username = data.player1 === my.username ? data.player2 : data.player1;
            if (lang === 'tr')
                showToast(`Chat maçı başladı! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'hi')
                showToast(`टूर्नामेंट मैच शुरू हो गया! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'pt')
                showToast(`Jogo de torneio começou! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else
                showToast(`Chat match started! ${player1.username} vs ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');

            render();
            showToast('Press Space to start the game', 'text-bg-primary', 'bi bi-exclamation-triangle-fill')

            document.addEventListener("keydown", SpaceKeyDown);

            console.log(`Match Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;

        case 'game.accept':
            player1.username = data.accepted;
            player2.username = data.accepter;
            my.game_id = data.game_id;
            if (data.accepter === my.username) {
                if (lang === 'tr')
                    showToast(`Davetiniz ${data.accepted} tarafından kabul edildi`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'hi')
                    showToast(`आपका निमंत्रण ${data.accepted} द्वारा स्वीकृत किया गया`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'pt')
                    showToast(`Seu convite foi aceito por ${data.accepted}`, 'text-bg-success', 'bi bi-check-circle-fill');
                else
                    showToast(`You accepted the game invitation from ${data.accepted}`, 'text-bg-success', 'bi bi-check-circle-fill');
                my.opponent_username = data.accepted; // if gerekir mi?
            }
            else if (data.accepted === my.username) {
                if (lang === 'tr')
                    showToast(`Davetiniz ${data.accepter} tarafından kabul edildi`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'hi')
                    showToast(`आपका निमंत्रण ${data.accepter} द्वारा स्वीकृत किया गया`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'pt')
                    showToast(`Seu convite foi aceito por ${data.accepter}`, 'text-bg-success', 'bi bi-check-circle-fill');
                else
                    showToast(`Your invitation is accepted by ${data.accepter}`, 'text-bg-success', 'bi bi-check-circle-fill');
                my.opponent_username = data.accepter; // if gerekir mi?
            }
            render();
            showToast('Press Space to start the game', 'text-bg-primary', 'bi bi-exclamation-triangle-fill');
            

            document.addEventListener("keydown", SpaceKeyDown);

            console.log(`Accepted Game Id: ${data.game_id} => ${data.accepted} vs ${data.accepter}`);
            break;

        case 'game.decline':
            if (data.declined === my.username) {    
                if (lang === 'tr')
                    showToast(`Davetiniz ${data.decliner} tarafından reddedildi`, 'text-bg-danger', 'bi bi-check-circle-fill'); 
                else if (lang === 'hi')
                    showToast(`आपका निमंत्रण ${data.decliner} द्वारा अस्वीकार किया गया`, 'text-bg-danger', 'bi bi-check-circle-fill');
                else if (lang === 'pt')
                    showToast(`Seu convite foi recusado por ${data.decliner}`, 'text-bg-danger', 'bi bi-check-circle-fill');
                else            
                    showToast(`Your invitation is declined by ${data.decliner}`, 'text-bg-danger', 'bi bi-check-circle-fill');
            }
            console.log(`Declined Game => ${data.declined} vs ${data.decliner}`);
            break;

        case 'game.start':
            // if they vote for Start, start the game otherwise update votes
            // Start the game
            checkbox.disabled = true;
            leftArea.style.display = 'none';
            if (data.vote == 2) {
                if (lang === 'tr')
                    showToast(`3 saniye içinde ${player1.username} ve ${player2.username} arasında oyun başlıyor`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'hi')
                    showToast(`3 सेकंड में ${player1.username} और ${player2.username} के बीच खेल शुरू हो रहा है`, 'text-bg-success', 'bi bi-check-circle-fill');
                else if (lang === 'pt')
                    showToast(`Jogo começando em 3 segundos entre ${player1.username} e ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
                else
                    showToast(`Game starting in 3 sec between ${player1.username} and ${player2.username}`, 'text-bg-success', 'bi bi-check-circle-fill');
                
                leaveButton.style.display = 'block';
                gameUtilsReset();
                
                // make invitationMessage disappear after 3 seconds
                
                leaveButton.onclick = function () {
                    leaveGame();
                    leaveButton.style.display = 'none';
                }
                
                // Control paddle1 with w, s keys
                document.addEventListener("keydown", function(event) {
                    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
                        upPressed = true;
                    } else if (event.key === "s" || event.key === "S"|| event.key === "ArrowDown") {
                        downPressed = true;
                    }
                    if (event.key === '1' && likeaCheaterCount < 1 && likeaCheater == "true" && (gameMode === "Abilities" || tournament === "abilities")) {
                        sendAbility("likeaCheater");
                        showToast('You used like a cheater!', 'text-bg-primary', 'bi bi-exclamation-triangle-fill');
                        likeaCheaterCount += 1;
                    }
                    else if (event.key === '2' && fastandFuriousCount < 1 && fastandFurious == "true" && isFrozenBallActive == false && (gameMode === "Abilities" || tournament === "abilities")) {
                        sendAbility("fastandFurious");
                        showToast('You used fast and furious!', 'text-bg-primary', 'bi bi-exclamation-triangle-fill');
                        fastandFuriousCount += 1;
                    }
                    else if (event.key === '3' && frozenBallCount < 1 && frozenBall == "true" && (gameMode === "Abilities" || tournament === "abilities")) {
                        sendAbility("frozenBall");
                        showToast('You used frozen ball!', 'text-bg-primary', 'bi bi-exclamation-triangle-fill');
                        isFrozenBallActive = true;
                        setTimeout(function () {
                            isFrozenBallActive = false;
                        }, 3000);
                        frozenBallCount += 1;
                    }
                });
                
                document.addEventListener("keyup", function(event) {
                    if (event.key === "w" || event.key === "W" || event.key === "ArrowUp") {
                        upPressed = false;
                    } else if (event.key === "s" || event.key === "S"|| event.key === "ArrowDown") {
                        downPressed = false;
                    }
                });

                setTimeout(function () {
                    startGame();
                }, 3000);
                // Ask ball coordinates every 16 milliseconds
                //setInterval(BallRequest, 16);

                console.log(`Started Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            }
            else if (data.vote == 1) {
                console.log(`Waiting for Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            }
            else if (data.vote == 0) {
                console.log(`None of the players hit space Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            }
            break;

        case 'game.leave':
            //clearInterval(BallRequest);
            leftArea.style.display = 'block';
            stopGame();
            var left_score = data.left_score;
            var opponent_score = data.opponent_score;
            var winner = data.winner;
            var loser = data.loser;
            document.getElementById('winnerText').innerText = winner;
            document.getElementById('loserText').innerText = loser;
            gameOverScreen.style.display = 'block';
            // Show some left game message with scores etc.
            //showToast(`${data.left} left the game. Winner is ${winner}`, 'text-bg-success', 'bi bi-check-circle-fill');
            // maybe put restart
            leaveButton.style.display = 'none';
            console.log(`Left Game Id: ${data.game_id}`);
            break;

        case 'game.end':
            //clearInterval(BallRequest);
            leftArea.style.display = 'block';
            stopGame();
            checkbox.disabled = false;
            player1.score = data.player1_score;
            player2.score = data.player2_score;
           
            var winner = data.winner;
            var loser = data.loser;
            console.log('Winner: ' + winner + ' Loser: ' + loser + ' Player1 score: ' + player1.score + ' Player2 score: ' + player2.score);
            document.getElementById('winnerText').innerText = winner;
            document.getElementById('loserText').innerText = loser;
            gameOverScreen.style.display = 'block';
            // Show some game ended message with scores etc
            if (lang === 'tr')
                showToast(`Oyun bitti. Kazanan ${data.winner}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'hi')
                showToast(`खेल समाप्त हो गया। विजेता ${data.winner}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else if (lang === 'pt')
                showToast(`O jogo acabou. Vencedor é ${data.winner}`, 'text-bg-success', 'bi bi-check-circle-fill');
            else
                showToast(`Game is ended. Winner is ${data.winner}`, 'text-bg-success', 'bi bi-check-circle-fill');
            // maybe put restart

            console.log(`Ended Game Id: ${data.game_id} => ${data.winner} won`);
            break;

        case 'game.pause':
            // Pause the game
            console.log('Game id: ' + data.game_id + ' paused');
            break;

        case 'game.resume':
            // Resume the game
            console.log('Game id: ' + data.game_id + ' resumed');
            break;
        
        case 'game.ball':
            //get ball position and update it
            ballMove(data.x, data.y)
            scoreUpdate(data.player1_score, data.player2_score)
            //console.log(`Moving Ball Id: ${data.game_id} for ball: ${data.x} ${data.y}`);
            break;

        case 'game.paddle':
            //get paddle position and update it
            paddleMove(data.player, data.y)
            //console.log(`Moving Paddle Id: ${data.game_id} for ${data.player}: ${data.y}`);
            break;

        case 'game.ability':
            console.log(data.ability + ' is used!')
            if (data.ability == 'giantMan' && (gameMode === "Abilities" || tournament === "abilities")) {
                if (data.player == player1.username)
                    paddle1.height = 115
                else if (data.player == player2.username)
                    paddle2.height = 115

            break;

    }};
}

matchsocket.sendJSON = function (data) {
    matchsocket.send(JSON.stringify(data));
}

function addUsersToTable(usersArray) {
    var tableBody = document.querySelector('.custom-table tbody');

    usersArray.forEach(function(username) {
        var row = document.createElement('tr');
        var usernameCell = document.createElement('td');
        usernameCell.textContent = username;
        var actionsCell = document.createElement('td');

        // Create buttons
        var btnGroup = document.createElement('div');
        btnGroup.className = "btn-group";
        btnGroup.style.display = "flex";
        btnGroup.style.justifyContent = "center";

        var inviteButton = document.createElement('button');
        inviteButton.type = "button";
        inviteButton.className = "invite-button";
        inviteButton.id = "inviteButton" + username;
        inviteButton.innerHTML = '<i class="bi bi-plus-circle-fill"></i>';

        var acceptButton = document.createElement('button');
        acceptButton.type = "button";
        acceptButton.className = "accept-button";
        acceptButton.id = "acceptButton" + username;
        acceptButton.innerHTML = '<i class="bi bi-patch-check-fill"></i>';

        var declineButton = document.createElement('button');
        declineButton.type = "button";
        declineButton.className = "decline-button";
        declineButton.id = "declineButton" + username;
        declineButton.innerHTML = '<i class="bi bi-x-circle-fill"></i>';

        // Add buttons to button group
        btnGroup.appendChild(inviteButton);
        btnGroup.appendChild(acceptButton);
        btnGroup.appendChild(declineButton);

        actionsCell.appendChild(btnGroup);
        row.appendChild(usernameCell);
        row.appendChild(actionsCell);
        tableBody.appendChild(row);

        // Add event listener to invite button
        inviteButton.addEventListener('click', function() {
            invite('false', username);
        });
    });
}

function removeUserFromTable(username) {
    var tableBody = document.querySelector('.custom-table tbody');
    var rows = tableBody.querySelectorAll('tr');

    rows.forEach(function(row) {
        var usernameCell = row.querySelector('td:first-child');
        if (usernameCell.textContent.trim() === username.trim()) {
            tableBody.removeChild(row);
        }
    });
}



function invite(matchmaking = 'false', username) {
    // Get necessary data and call socket.sendJSON
    if (lang === 'tr')
        showToast(`Oyuna ${username} davet ettiniz`, 'text-bg-success', 'bi bi-check-circle-fill')
    else if (lang === 'hi')
        showToast(`आपने ${username} को एक खेल के लिए आमंत्रित किया`, 'text-bg-success', 'bi bi-check-circle-fill')
    else if (lang === 'pt')
        showToast(`Você convidou ${username} para um jogo`, 'text-bg-success', 'bi bi-check-circle-fill')
    else
        showToast(`You invited ${username} to a game`, 'text-bg-success', 'bi bi-check-circle-fill')
    matchsocket.sendJSON({
        action: 'invite',
        matchmaking: matchmaking,
        invitee_username: username,
    });
}

matchmakingButton.onclick = function () {
    invite('true', '');
}

//----------------------------------------------

function hideInviteButtons(username1, username2) {
    // Get the invite buttons for the two users
    const inviteButton1 = document.getElementById(`inviteButton${username1}`);
    const inviteButton2 = document.getElementById(`inviteButton${username2}`);

    // Hide the invite buttons
    if (inviteButton1) inviteButton1.style.display = 'none';
    if (inviteButton2) inviteButton2.style.display = 'none';
}

function exitGame() {
    console.log("id: " + my.game_id);
    matchsocket.sendJSON({
        action: 'exit',
        game_id: my.game_id,
    });
    
    swapApp('/pong-game-find')
}

function accept(inviter) {
    // Get necessary data and call socket.sendJSON
    matchsocket.sendJSON({
        action: 'accept',
        inviter_username: inviter,
            });
}

function decline(inviter) {
    // Get necessary data and call socket.sendJSON
    matchsocket.sendJSON({
        action: 'decline',
        inviter_username: inviter,
    });
}

// Vote count ll be 1 at start if 
function startRequest(player1, player2) {
    matchsocket.sendJSON({
        action: 'start.request',
        game_id: my.game_id,
        opponent: my.opponent_username,
        vote: 1,
    });
}

function SpaceKeyDown(event) {
    if (event.code === "Space") {
        startRequest(my.username, my.opponent_username);
        // Remove the event listener after it has been triggered once
        document.removeEventListener("keydown", SpaceKeyDown);
    }
}


function leaveGame() {
    matchsocket.sendJSON({
        action: 'leave.game',
        game_id: my.game_id,
        left: my.username,
        opponent: my.opponent_username,
    });
}

// send this in keydown event
function PaddleRequest(direction) {
    // Get necessary data and call socket.sendJSON
    matchsocket.sendJSON({
        action: 'paddle',
        game_id: my.game_id,
        direction: direction
    });
}

function updatePaddlePosition() {
    if (upPressed) {
        PaddleRequest('up');
    } else if (downPressed) {
        PaddleRequest('down');
    }
}

function sendAbility(ability) {
    matchsocket.sendJSON({
        action: 'ability',
        abilities: ability,
        game_id: my.game_id,
    });
}



// send this in setInterval(update, 16) this ll be game state
function BallRequest() {
    // Get necessary data and call socket.sendJSON
    matchsocket.sendJSON({
        action: 'ball',
        game_id: my.game_id,
    });
}

document.getElementById('exitButton').addEventListener('click', exitGame);

checkbox.addEventListener('change', function() {
    // Checkbox'un durumuna göre etiketin innerHTML değerini değiştirme
    if (checkbox.checked) {
        gameMode = "Abilities";
        if (lang === 'tr')
            selectedGameModeLabel.innerHTML = "Yetenekler";
        else if (lang === 'hi')
            selectedGameModeLabel.innerHTML = "क्षमताएँ";
        else if (lang === 'pt')
            selectedGameModeLabel.innerHTML = "Habilidades";
        else
            selectedGameModeLabel.innerHTML = "Abilities";
    } else {
        gameMode = "Vanilla";
        if (lang === 'tr')
            selectedGameModeLabel.innerHTML = "Vanilya";
        else if (lang === 'hi')
            selectedGameModeLabel.innerHTML = "वैनिला";
        else if (lang === 'pt')
            selectedGameModeLabel.innerHTML = "Baunilha";
        else
            selectedGameModeLabel.innerHTML = "Vanilla";
    }
});

const gameModeSelect = document.getElementById("gameModeSelect");

gameModeSelect.addEventListener("mouseenter", function() {
    document.querySelector(".game-mode-info").style.display = "block";
});

gameModeSelect.addEventListener("mouseleave", function() {
    document.querySelector(".game-mode-info").style.display = "none";
});
}