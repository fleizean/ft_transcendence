// sockpong.js
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');  // Replace with your WebSocket endpoint


const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

var my = {
    username: '', game_id: '', tournament_id: '', group_name: '',
}

socket.onopen = function (e) {
    console.log('WebSocket connection established');
}

socket.onclose = function (e) {
    if (my.game_id) {
        socket.sendJSON({
            action: 'leave.match',
            game_id: my.game_id,
            player: my.username,
        });
    }
    else if (my.tournament_id) {
        socket.sendJSON({
            action: 'leave.tournament',
            tournament_id: my.tournament_id,
            player: my.username,
        });
    }
    console.error('WebSocket connection closed');
}

socket.onerror = function (e) {
    console.error('Error: ' + e.data);
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
            for (let user of data.users) {
                console.log('', user);
                onlineUsersTable.innerHTML += `<tr><th>${user}</th></tr>`;
            }
            my.username = data.username;
            console.log('Player connected:', data.username);
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
            my.group_name = data.group_name;
            if (data.invited === my.username) {
                invitationMessage.textContent = `You received a game invitation from ${data.inviter}. Do you want to accept?`;
                invitationModal.style.display = 'block';
            }
            else
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
            if (data.accepter === my.username) {
                invitationMessage.textContent = `You accepted the game invitation from ${data.accepted}`;
                invitationMessage.style.display = 'block';
            }
            else if (data.accepted === my.username) {
                invitationMessage.textContent = `Your invitation is accepted by ${data.accepter}`;
                invitationMessage.style.display = 'block';
            }
            my.game_id = data.game_id;
            // Show the game screen and start button

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
            
            console.log(`Started Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;
        case 'game.leave':
            console.log(`Left Game Id: ${data.game_id} as ${data.player}`);
            break;
        case 'game.paddle.move':
            console.log(`Moving Paddle Id: ${data.game_id} for ${data.player}: ${data.x} ${data.y}`);
            break;
        case 'game.ball.move':
            console.log(`Moving Ball Id: ${data.game_id} for ball: ${data.x} ${data.y}`);
            break;
        // What about draw?
        case 'game.end':
            console.log(`Ended Game Id: ${data.game_id} => ${data.winner} won`);
            break;
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

const voteCount = document.getElementById('vote_count');
voteCount.value = 0; // default value 0
const startButton = document.getElementById('startButton');
const onlineUsersTable = document.getElementById('OnlineUsers');
const invitationModal = document.getElementById('gameInvitationModal');
const invitationMessage = document.getElementById('invitationMessage');
const acceptButton = document.getElementById('acceptButton');
const declineButton = document.getElementById('declineButton');
invitationModal.style.display = 'none';
invitationMessage.style.display = 'none';

// Add an event listener for the "Invite" button
const inviteButton = document.getElementById('inviteButton');
const inviteInput = document.getElementById('inviteInput');
inviteButton.onclick = function () {
    invitationMessage.style.display = 'block';
    invite();
}

function invite() {
    // Get necessary data and call socket.sendJSON
    username = inviteInput.value;
    // maybe put in action.js
    socket.sendJSON({
        action: 'invite',
        invited: username,
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

function startGame() {
    var vote_count = voteCount.value;
    vote_count += 1;
    socket.sendJSON({
        action: 'game.start',
        game_id: 'game_id',
        group_name: my.g,
        player1: 'player1_username',
        player2: 'player2_username',
        vote_count: vote_count,
    });
}

// send this in setInterval(update, 16) this ll be game state
function movePaddle() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'paddle.move',
        game_id: 'game_id',
        y: 1, // if this for paddle only y required and for ball both
        player: 'username', // player1 or player2
    });
}

// send this in setInterval(update, 16) this ll be game state
function moveBall() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'ball.move',
        game_id: 'game_id',
        x: 1, // if this for paddle only y required and for ball both
        y: -1,
    });
}



function endGame() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'end',
        game_id: 'game_id',
        player1_score: 1, // send scores when game ended
        player2_score: 2,
    });
}

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










