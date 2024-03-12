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
    username: '', opponent_username: '', game_id: '', vote: -1, tournament_id: '', 
};


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

var requestId;

// The main game loop
var startGame = function () {
    render();
    // Request to do this again ASAP
    requestId = requestAnimationFrame(startGame);
};

// When you want to stop the game loop
var stopGame = function() {
    cancelAnimationFrame(requestId);
};

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
    clearInterval(BallRequest);
    stopGame();
    console.error('WebSocket connection closed');
}

matchsocket.onerror = function (e) {
    console.error('Error: ' + e.data);
    clearInterval(BallRequest);
    stopGame();
}

matchsocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
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
            showToast(data.user + ' joined!', 'text-bg-success', 'bi bi-check-circle-fill')
        break;

        case 'user.outlobby':
            // Send others user left the lobby
            console.log('User out lobby', data.user);
            // Remove user from online users list
            removeUserFromTable(data.user);
            showToast(data.user + ' left!', 'text-bg-danger', 'bi bi-check-circle-fill')
            break;

        case 'game.invite':
            // Tell user that he/she is invited to a game
            console.log('Game invite', data.inviter);
            console.log('data: ', data.invitee + " " + my.username)
            // Display the modal for accepting or declining the invitation
            if (data.invitee === my.username)  {
                showToast(`You received a game invitation from ${data.inviter}`, 'text-bg-success', 'bi bi-check-circle-fill')
                document.getElementById(`acceptButton${data.inviter}`).style.display = 'flex';
                document.getElementById(`declineButton${data.inviter}`).style.display = 'flex';
            }

            document.getElementById(`acceptButton${data.inviter}`).onclick = function () {
                accept(data.inviter);
                document.getElementById(`acceptButton${data.inviter}`).style.display = 'none';
                document.getElementById(`declineButton${data.inviter}`).style.display = 'none';
            };

            document.getElementById(`declineButton${data.inviter}`).onclick = function () {
                decline(data.inviter);
                document.getElementById(`acceptButton${data.inviter}`).style.display = 'none';
                document.getElementById(`declineButton${data.inviter}`).style.display = 'none';
            };

            console.log(`Invited Group: ${data.inviter} vs ${data.invitee}`);
            break;
        
        case 'game.accept':
            player1.username = data.accepted;
            player2.username = data.accepter;
            if (data.accepter === my.username) {
                invitationMessage.textContent = `You accepted the game invitation from ${data.accepted}`;
                invitationMessage.style.display = 'block';
                my.opponent_username = data.accepted; // if gerekir mi?
            }
            else if (data.accepted === my.username) {
                invitationMessage.textContent = `Your invitation is accepted by ${data.accepter}`;
                invitationMessage.style.display = 'block';
                my.opponent_username = data.accepter; // if gerekir mi?
            }
            if (my.game_id === '')
                my.game_id = data.game_id;
            // Show the game start screen and start button
            startModal.style.display = 'block';
            startButton.onclick = function () {
                // maybe put timeout here for protection against bashing button
                startRequest(my.username, my.opponent_username);
            };
            render();
            console.log(`Accepted Game Id: ${data.game_id} => ${data.accepted} vs ${data.accepter}`);
            break;

        case 'game.decline':
            if (data.decliner === my.username) {
                invitationMessage.textContent = `You declined the game invitation from ${data.declined}`;
                invitationMessage.style.display = 'block';
            }
            else if (data.declined === my.username) {
                invitationMessage.textContent = `Your invitation is declined by ${data.decliner}`;
                invitationMessage.style.display = 'block';
            }
            console.log(`Declined Game => ${data.declined} vs ${data.decliner}`);
            break;

        case 'game.start':
            // if they vote for Start, start the game otherwise update votes
            // Start the game
            if (data.vote == 2) {
                myCheckMark.style.display = 'block';
                opCheckMark.style.display = 'block';
                invitationMessage.textContent = `Game starting in 3 sec between ${data.player1} and ${data.player2}`;
                setTimeout(function () {
                  invitationMessage.style.display = "none";
                  myCheckMark.style.display = "none";
                  opCheckMark.style.display = "none";
                }, 3000);
                startModal.style.display = 'none';

                leaveButton.style.display = 'block';
                // make invitationMessage disappear after 3 seconds

                leaveButton.onclick = function () {
                    leaveGame();
                    leaveButton.style.display = 'none';
                }

                // Control paddle1 with w, s keys
                document.addEventListener("keydown", function(event) {
                    if (event.key === "w" || event.key === "ArrowUp") {
                        PaddleRequest("up");
                    } else if (event.key === "s" || event.key === "ArrowDown") {
                        PaddleRequest("down");
                    }
                });
                // Ask ball coordinates every 16 milliseconds
                startGame();
                setInterval(BallRequest, 16);

                console.log(`Started Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            }
            else if (data.vote == 1) {
                if (myCheckMark.style.display == 'none')
                    opCheckMark.style.display = 'block';
                else if (opCheckMark.style.display == 'none')
                    myCheckMark.style.display = 'block';
                console.log(`Waiting for Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            }
            else if (data.vote == 0) {
                opCheckMark.style.display = 'none';
                myCheckMark.style.display = 'none';
            }
            break;

        case 'game.leave':
            clearInterval(BallRequest);
            stopGame();
            left_score = data.left_score;
            opponent_score = data.opponent_score;
            winner = data.winner;
            // Show some left game message with scores etc.
            invitationMessage.textContent = `${data.left} left the game. Winner is ${data.winner}`;
            invitationMessage.style.display = 'block';
            // maybe put restart
            restartButton.style.display = 'block';
            restartButton.onclick = function () {
                startRequest(my.username, my.opponent_username);
            };

            console.log(`Left Game Id: ${data.game_id}`);
            break;

        case 'game.end':
            clearInterval(BallRequest);
            stopGame();
            player1_score = data.player1_score;
            player2_score = data.player2_score;
            winner = data.winner;
            loser = data.loser;
            // Show some game ended message with scores etc.
            invitationMessage.textContent = `Game is ended. Winner is ${data.winner}`;
            invitationMessage.style.display = 'block';
            // maybe put restart
            restartButton.style.display = 'block';
            restartButton.onclick = function () {
                //restartRequest(my.username, my.opponent_username);
                //startRequest(my.username, my.opponent_username);
            };
            console.log(`Ended Game Id: ${data.game_id} => ${data.winner} won`);
            break;
        //? not sure
        case 'game.restart':
            // Send restart invite to user
            console.log('Restart Requester: ' + data.inviter);
            break;

        case 'game.exit':
            // Tell both user that game is ended and show scores and winner
            console.log('Game id: ' + data.game_id + ' player1_score: ' + data.player1_score + ' player2_score: ' + data.player2_score + ' winner: ' + data.winner + ' loser: ' + data.loser);
            break;

        case 'game.pause':
            // Pause the game
            console.log('Game id: ' + data.game_id + ' paused');
            break;

        case 'game.resume':
            // Resume the game
            console.log('Game id: ' + data.game_id + ' resumed');
            break;
        
        case 'user.reconnected': //? not sure
            // Tell other user that i reconnected
            console.log('User reconnected', data.user);
            break;

        case 'game.ball':
            //get ball position and update it
            ballMove(data.x, data.y)
            scoreUpdate(data.player1_score, data.player2_score)
            console.log(`Moving Ball Id: ${data.game_id} for ball: ${data.x} ${data.y}`);
            break;

        case 'game.paddle':
            //get paddle position and update it
            paddleMove(data.player, data.y)
            console.log(`Moving Paddle Id: ${data.game_id} for ${data.player}: ${data.y}`);
            break;

        

    }};


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
        actionsCell.innerHTML = `
        <div class="btn-group" style="display:flex; justify-content:center;">
            <button type="button" class="invite-button" onclick="invite('false', '${username}')"><i class="bi bi-plus-circle-fill"></i></button>
            <button type"button" class="accept-button" id="acceptButton${username}"><i class="bi bi-patch-check-fill"></i></button>
            <button type="button" class="decline-button" id="declineButton${username}"><i class="bi bi-x-circle-fill"></i></button>
        </div>
            `;
        row.appendChild(usernameCell);
        row.appendChild(actionsCell);
        tableBody.appendChild(row);
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

//----------------------------------------------
// Add an event listener for the "Matchmaking" button
/* inviteButton.onclick = function () {
    invite('true');
} */

function invite(matchmaking = 'false', username) {
    // Get necessary data and call socket.sendJSON
    showToast(`You invited ${username} to a game`, 'text-bg-success', 'bi bi-check-circle-fill')
    matchsocket.sendJSON({
        action: 'invite',
        matchmaking: matchmaking,
        invitee_username: username,
    });
}

//----------------------------------------------

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
    my.vote *= -1
    myCheckMark.style.display = 'block';
    if (my.vote == -1){
        myCheckMark.style.display = 'none';
    }
    matchsocket.sendJSON({
        action: 'start.request',
        game_id: my.game_id,
        opponent: my.opponent_username,
        vote: my.vote,
    });
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

// send this in setInterval(update, 16) this ll be game state
function BallRequest() {
    // Get necessary data and call socket.sendJSON
    matchsocket.sendJSON({
        action: 'ball',
        game_id: my.game_id,
    });
}