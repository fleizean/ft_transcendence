// sockpong.js
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');  // Replace with your WebSocket endpoint


const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

// Paddle objects
var paddleWidth = 10;
var paddleHeight = 75;
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
}

// Draw everything
function render() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = "#0095DD";
    context.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    context.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);

    context.beginPath();
    context.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2, false);
    context.fill();
    context.closePath();

    context.font = "16px Arial";
    context.fillText(player1.username + ": " + player1.score, 10, 20);
    context.fillText(player2.username + ": " + player2.score, canvas.width - 85, 20);
}


const startModal = document.getElementById('startModal');
startModal.style.display = 'none';
const myCheckMark = document.getElementById('myCheckMark');
myCheckMark.style.display = 'none';
const opCheckMark = document.getElementById('opCheckMark');
opCheckMark.style.display = 'none';
/* const voteCount = document.getElementById('voteCount');
voteCount.value = -1; */
const startButton = document.getElementById('startButton');
const leaveButton = document.getElementById('leaveButton');
const restartButton = document.getElementById('restartButton');
const onlineUsersTable = document.getElementById('OnlineUsers');
const invitationModal = document.getElementById('gameInvitationModal');
const invitationMessage = document.getElementById('invitationMessage');
const acceptButton = document.getElementById('acceptButton');
const declineButton = document.getElementById('declineButton');
const inviteButton = document.getElementById('inviteButton');
const inviteInput = document.getElementById('inviteInput');
invitationModal.style.display = 'none';
invitationMessage.style.display = 'block';
leaveButton.style.display = 'none';
restartButton.style.display = 'none';



socket.onopen = function (e) {
    // Show some greeting message
    console.log('WebSocket connection established');
}

socket.onclose = function (e) {
    clearInterval(BallRequest);
    stopGame();
    console.error('WebSocket connection closed');
    if (my.game_id) {
        // Show some connection lost message with scores etc.
    }
    else if (my.tournament_id && my.game_id) {
        // Show some connection lost message with scores and tournament rank etc.
    }
}

socket.onerror = function (e) {
    console.error('Error: ' + e.data);
    clearInterval(BallRequest);
    stopGame();
    if (!inviteInput.value) {
        invitationMessage.textContent = e.data;
        invitationModal.style.display = 'block';
    }
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    switch (data.type) {
        case 'user.online':
            // Add username to onlineUsers table
            onlineUsersTable.innerHTML = '';
            //showOnlineUsers(data.users);
            for (let user of data.users) {
                console.log('', user);
                onlineUsersTable.innerHTML += `<tr><th>${user}</th></tr>`;
            }
            if (my.username === '')
                my.username = data.username;
            console.log('Player connected:', data.username);
            console.log(my.username);
            break;
        case 'user.offline':
            // Remove username from onlineUsers table
            //onlineUsersTable.innerHTML = '';
            // Get onlineUser table remove the line which username in it
            onlineUsersTable.innerHTML = onlineUsersTable.innerHTML.replace(`<tr><th>${data.username}</th></tr>`, '');

/*             for (let user of data.users) {
                onlineUsersTable.innerHTML += `<tr><th>${user}</th></tr>`;
            } */
            console.log('Player disconnected:', data.username);
            break;
        
        case 'game.invite':
            // Display the modal for accepting or declining the invitation
            console.log(my.username);
            if (data.invited === my.username) {
                invitationMessage.textContent = `You received a game invitation from ${data.inviter}`;
                invitationModal.style.display = 'block';
            }
            if (data.inviter === my.username)
            {
                invitationMessage.textContent = `You send a game invitation to ${data.invited}`;
            }

            acceptButton.onclick = function () {
                accept(data.group_name, data.inviter, data.invited);
                invitationModal.style.display = 'none';
            };

            declineButton.onclick = function () {
                decline(data.group_name, data.inviter, data.invited);
                invitationModal.style.display = 'none';
            };

            console.log(`Invited Group Name: ${data.group_name} => ${data.inviter} vs ${data.invited}`);
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
            // Show the game screen and start button
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
        // What about draw?
        case 'game.end':
            clearInterval(BallRequest);
            stopGame();
            player1_score = data.player1_score;
            player2_score = data.player2_score;
            winner = data.winner;
            // Show some game ended message with scores etc.
            invitationMessage.textContent = `Game is ended. Winner is ${data.winner}`;
            invitationMessage.style.display = 'block';
            // maybe put restart
            restartButton.style.display = 'block';
            restartButton.onclick = function () {
                startRequest(my.username, my.opponent_username);
            };
            console.log(`Ended Game Id: ${data.game_id} => ${data.winner} won`);
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

        
        
            // Tournament cases
        case 'tournament.start':
            for (const match in data.matches) {
                console.log(`Started Tournament Id: ${data.tournament_id} => Match Id: ${match.match_id} => ${match.player1} vs ${match.player2}`);
            }
            break;
        case 'tournament.join':
            console.log(`Joined Tournament Id: ${data.tournament_id} as ${data.player}`);
            break;
        case 'tournament.finish':
            console.log(`Finished Match Id: ${data.match_id} => ${data.winner} won`);
            break;
        case 'tournament.next':
            for (const match in data.matches) {
                console.log(`Tournament Id: ${data.tournament_id} => Next Match Id: ${match.match_id} => ${match.player1} vs ${match.player2}`);
            }
            break;
        case 'tournament.end':
            console.log(`Ended Tournament Id: ${data.tournament_id} => ${data.winner} won tournament`);
            break;
        case 'tournament.cancel':
            console.log(`Cancelled Tournament Id: ${data.tournament_id}`);
            break;
        // leave can be added also for match or user.offline would be enough
        case 'tournament.leave':
            console.log(`Left Tournament Id: ${data.tournament_id} as ${data.player}`);
            break;
        }
    }
    
socket.sendJSON = function (data) {
    socket.send(JSON.stringify(data));
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

/* function showOnlineUsers(users) {
    for (let user of users) {
        let listItem = document.createElement('div');
        listItem.className = 'list-group-item';

        // Create the status icon
        let statusIcon = document.createElement('span');
        statusIcon.className = 'badge ' + 'bg-success';//(user.status == 'online' ? 'bg-success' : (user.status == 'waiting' ? 'bg-warning' : 'bg-danger'));
        statusIcon.dataset.bsToggle = 'tooltip';
        statusIcon.dataset.bsPlacement = 'top';
        statusIcon.title = 'online';
        statusIcon.textContent = '•';
        listItem.appendChild(statusIcon);

        // Add the username
        let usernameText = document.createTextNode(' ' + user);
        listItem.appendChild(usernameText);

        // Create the invite button
        if (user !== my.username){
            let inviteButton = document.createElement('button');
            inviteButton.className = 'btn btn-primary btn-sm float-end';
            inviteButton.onclick = function() { invite(user); };
            inviteButton.textContent = 'Invite';
            listItem.appendChild(inviteButton);
        }
        // Add the list item to the online users list
        onlineUsersTable.appendChild(listItem);
    }
};

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
 */

// Add an event listener for the "Invite" button
inviteButton.onclick = function () {
    invitationMessage.style.display = 'block';
    invite();
}

function invite() {
    // Get necessary data and call socket.sendJSON
    //username = inviteInput.value;
    // maybe put in action.js
    socket.sendJSON({
        action: 'invite',
        invited: inviteInput.value,
    });
}

function accept(group_name, inviter, invited) {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'accept',
        group_name: group_name,
        accepted: inviter,
        accepter: invited,
    });
}

function decline(group_name, inviter, invited) {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'decline',
        group_name: group_name,
        declined: inviter,
        decliner : invited,
    });
}
// Vote count ll be 1 at start if 
function startRequest(player1, player2) {
    my.vote *= -1
    myCheckMark.style.display = 'block';
    if (my.vote == -1){
        myCheckMark.style.display = 'none';
    }
    socket.sendJSON({
        action: 'start.request',
        game_id: my.game_id,
        player1: player1,
        player2: player2,
        vote: my.vote,
    });
}

// We need to store game scores in server side
function leaveGame() {
    socket.sendJSON({
        action: 'leave.game',
        game_id: my.game_id,
        left: my.username,
        opponent: my.opponent_username,
    });
}

// When game ended send this only once 
/* function gameEnded() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'end',
        game_id: my.game_id,
    });
} */

// send this in keydown event
function PaddleRequest(direction) {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'paddle',
        game_id: my.game_id,
        direction: direction
    });
}

// send this in setInterval(update, 16) this ll be game state
function BallRequest() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'ball',
        game_id: my.game_id,
    });
}


// Tournament functions---------------------------------------------

function create() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'create',
        name: 'tournament_name' // When create clicked take tournament_name somehow
    });
}

function join() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'join',
        tournament_id: 'tournament_id', // When join clicked take tournament_id somehow
        username: 'username', // When join clicked take username somehow
    });
}

function cancel() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'cancel',
        tournament_id: 'tournament_id',
    });
}

function tournamentMatchLeft() {
    socket.sendJSON({
        action: 'leave.tournament',
        tournament_id: my.tournament_id,
        game_id: my.game_id,
        left: my.username,
        opponent: my.opponent_username,
        left_score: 0, // send scores when game ended
        opponent_score: 0,
    });
}

function leave() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'leave',
        tournament_id: 'tournament_id',
        player: 'username', // When leave clicked take username somehow
    });
}

function startTournament() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'start',
        tournament_id: 'tournament_id', // When start clicked create and take tournament_id somehow
        mathces: [
            {
                match_id: 'match_id', // When start clicked create and take match_id somehow
                player1: 'player1_username',
                player2: 'player2_username',
            },
            {
                match_id: 'match_id',
                player1: 'player3_username',
                player2: 'player4_username',
            },
        ], // When start clicked create and take matches somehow
    });
}

function finish() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'finish',
        match_id: 'match_id',
        winner: 'username', // player1 or player2
    });
}

function next() {
    // Get necessary data and call socket.sendJSON
    // next games
    socket.sendJSON({
        action: 'next',
        tournament_id: 'tournament_id',
        matches: [
            {
                match_id: 'match_id',
                player1: 'player1_username',
                player2: 'player2_username',
            },
            {
                match_id: 'match_id',
                player1: 'player3_username',
                player2: 'player4_username',
            },
        ],
    });
    
    
    // tournament ended no next
    socket.sendJSON({
        action: 'next',
        tournament_id: 'tournament_id',
        winner: 'username', // player1 or player2
    });
}










