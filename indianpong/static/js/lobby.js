// sockpong.js
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');  // Replace with your WebSocket endpoint


const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

/* const startModal = document.getElementById('startModal');
startModal.style.display = 'none';
const voteCount = document.getElementById('voteCount');
voteCount.value = -1;
const startButton = document.getElementById('startButton');
const onlineUsersTable = document.getElementById('OnlineUsers');
const invitationModal = document.getElementById('gameInvitationModal');
const invitationMessage = document.getElementById('invitationMessage');
const acceptButton = document.getElementById('acceptButton');
const declineButton = document.getElementById('declineButton');
const inviteButton = document.getElementById('inviteButton');
const inviteInput = document.getElementById('inviteInput');
invitationModal.style.display = 'none';
invitationMessage.style.display = 'none'; */

var my = {
    username: '', opponent_username: '', game_id: '', tournament_id: '', group_name: '',
}

socket.onopen = function (e) {
    // Show some greeting message
    console.log('WebSocket connection established');
}

socket.onclose = function (e) {
    if (my.game_id) {
        // Show some connection lost message with scores etc.
    }
    else if (my.tournament_id && my.game_id) {
        // Show some connection lost message with scores and tournament rank etc.
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
            if (my.username === '')
                my.username = data.username;
            // Add username to onlineUsers table
            //onlineUsersTable.innerHTML = '';
            showOnlineUsers(data.users);
/*             for (let user of data.users) {
                console.log('', user);
                onlineUsersTable.innerHTML += `<tr><th>${user}</th></tr>`;
            } */
            console.log('Player connected:', data.username);
            console.log(my.username);
            break;
        case 'user.offline':
            // Remove username from onlineUsers table
            //onlineUsersTable.innerHTML = '';
            // Get onlineUser table remove the line which username in it
            document.querySelectorAll('#userTableBody td').forEach(cell => {
                if (cell.textContent === data.username)
                    cell.closest('tr').remove();
            }
            );
            //onlineUsersTable.innerHTML = onlineUsersTable.innerHTML.replace(`<tr><th>${data.username}</th></tr>`, '');

/*             for (let user of data.users) {
                onlineUsersTable.innerHTML += `<tr><th>${user}</th></tr>`;
            } */
            console.log('Player disconnected:', data.username);
            break;
        
        case 'game.invite':
            // Display the modal for accepting or declining the invitation
            if (my.group_name === '')
                my.group_name = data.group_name;
            console.log(my.username);
            if (data.invited === my.username) {
                document.getElementById('message').innerText = `You received a game invitation from ${data.inviter}.`;
                const acceptBtn = document.createElement('button');
                acceptBtn.classList.add('btn', 'btn-success', 'accept-btn');
                acceptBtn.innerText = 'Accept';
        
                // Create Decline button
                const declineBtn = document.createElement('button');
                declineBtn.classList.add('btn', 'btn-danger', 'decline-btn');
                declineBtn.innerText = 'Decline';
    
                const inviteButton = document.querySelector('.invite-btn[data-username="' + data.inviter + '"]');
                inviteButton.style.display = 'none';
                // Insert Accept and Decline buttons after the hidden Invite button
                inviteButton.parentNode.insertBefore(acceptBtn, inviteButton.nextSibling);
                inviteButton.parentNode.insertBefore(declineBtn, inviteButton.nextSibling);
        
/*              invitationMessage.textContent = `You received a game invitation from ${data.inviter}.`; //Do you want to accept?`
                invitationModal.style.display = 'block'; */
            }
/*             else
            {
                document.getElementById('message').innerText = `You sent a game invitation to ${data.invited}`;
                //invitationMessage.textContent = `You send a game invitation to ${data.invited}`;
            } */
            document.addEventListener('click', function (event) {
                if (event.target.classList.contains('accept-btn') || event.target.classList.contains('decline-btn')) {
                    // Simulate backend logic for accepting or declining the invitation
                    if (event.target.classList.contains('accept-btn')) {
                        accept(data.group_name, data.inviter, data.invited);
                    }
                    else if (event.target.classList.contains('decline-btn')) {
                        decline(data.group_name, data.inviter, data.invited);
                    }
                    // Hide accept and decline buttons show start button

                }
            });

/*             acceptButton.onclick = function () {
                accept(data.group_name, data.inviter, data.invited);
                invitationModal.style.display = 'none';
            };

            declineButton.onclick = function () {
                decline(data.group_name, data.inviter, data.invited);
                invitationModal.style.display = 'none';
            }; */

            console.log(`Invited Group Name: ${data.group_name} => ${data.inviter} vs ${data.invited}`);
            break;
            case 'game.accept':
            // Create Start button and replace with Accept button and Decline button
            const startBtn = document.createElement('button');
            startBtn.classList.add('btn', 'btn-success', 'start-btn');
            startBtn.innerText = 'Start';
            if (data.accepter === my.username) {
                /*                 invitationMessage.textContent = `You accepted the game invitation from ${data.accepted}`;
                invitationMessage.style.display = 'block'; */
                document.getElementById('message').innerText = `You accepted the game invitation from ${data.accepted}`;
                my.opponent_username = data.accepted; // if gerekir mi?
                const acceptButton = document.querySelector('.accept-btn');
                acceptButton.style.display = 'none';
                const declineButton = document.querySelector('.decline-btn');
                declineButton.style.display = 'none';
                // Insert Start button after the hidden Decline button
                declineButton.parentNode.insertBefore(startBtn, declineButton.nextSibling);
            }
            else if (data.accepted === my.username) {
/*                 invitationMessage.textContent = `Your invitation is accepted by ${data.accepter}`;
                invitationMessage.style.display = 'block'; */
                document.getElementById('message').innerText = `Your invitation is accepted by ${data.accepter}`;
                my.opponent_username = data.accepter; // if gerekir mi?
                const inviteButton = querySelector('.invite-btn[data-username="' + data.accepter + '"]')
                //insert Start button after the hidden Invite button
                inviteButton.parentNode.insertBefore(startBtn, inviteButton.nextSibling);
            }
            if (my.game_id === '')
                my.game_id = data.game_id;


            // Show the game screen and start button
/*             startModal.style.display = 'block';
            startButton.onclick = function () {
                startRequest(my.username, my.opponent_username);
            }; */

            console.log(`Accepted Game Id: ${data.game_id} => ${data.accepted} vs ${data.accepter}`);
            break;
        case 'game.decline':
            if (data.decliner === my.username) {
/*                 invitationMessage.textContent = `You declined the game invitation from ${data.declined}`;
                invitationMessage.style.display = 'block'; */
                document.getElementById('message').innerText = `You declined the game invitation from ${data.declined}`;
            }
            else if (data.declined === my.username) {
/*                 invitationMessage.textContent = `Your invitation is declined by ${data.decliner}`;
                invitationMessage.style.display = 'block'; */
                document.getElementById('message').innerText = `Your invitation is declined by ${data.decliner}`;
            }
            console.log(`Declined Game => ${data.declined} vs ${data.decliner}`);
            break;
        case 'game.start':
            // Start the game
            invitationMessage.textContent = `Game started between ${data.player1} and ${data.player2}`;
            console.log(`Started Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;
        case 'game.leave':
            my.score = data.score;
            my.opponent_score = data.opponent_score;
            winner = data.winner;
            // Show some left game message with scores etc.
        
            console.log(`Left Game Id: ${data.game_id} => ${my.opponent_username} left`);
            break;
        // What about draw?
        case 'game.end':
            my.score = data.score;
            my.opponent_score = data.opponent_score;
            winner = data.winner;
            console.log(`Ended Game Id: ${data.game_id} => ${data.winner} won`);
            break;
        case 'game.ball.move':
            //get ball position and update it
            ballDraw(data.x, data.y)
            

            console.log(`Moving Ball Id: ${data.game_id} for ball: ${data.x} ${data.y}`);
            break;
        case 'game.paddle.move':
            //get paddle position and update it
            paddleDraw(data.player, data.y)
            console.log(`Moving Paddle Id: ${data.game_id} for ${data.player}: ${data.y}`);
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

function showOnlineUsers(users) {
    const tbody = document.getElementById('userTableBody');
    tbody.innerHTML = '';
    users.forEach(user => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${user}</td>
        <td>
          <span class="status-icon bg-success" title="Online"></span>
          Online
        </td>`;
      if (user !== my.username){
          row.innerHTML += `
            <td>
              <button class="btn btn-primary invite-btn" data-username="${user}">Invite</button>
            </td>
          `;
      }
      tbody.appendChild(row);
    });

}
// Add your JavaScript logic here

document.getElementById('userTableBody').addEventListener('click', function (event) {
    const clickedButton = event.target;

    if (clickedButton.classList.contains('invite-btn')) {
        const username = clickedButton.getAttribute('data-username');

        // Call your invite function with the username
        invite(username);

        // Hide invite button
        clickedButton.style.display = 'none';

        // Show appropriate message
        document.getElementById('message').innerText = `You sent a game invitation to ${username}`;
    }
});


/*   button.addEventListener('click', function (event) {
    const username = this.getAttribute('data-username');
    // Call your invite function with the username
    invite(username);

    // Show appropriate message
    document.getElementById('message').innerText = `You sent a game invitation to ${username}`;
    // Hide invite button
    this.style.display = 'none';
    // Show accept and decline buttons
    const actionCol = event.currentTarget.closest('tr').querySelector('.action-col');
    actionCol.innerHTML = `
        <button class="btn btn-success start-btn">Accept</button>
        <button class="btn btn-danger decline-btn">Decline</button>
    `;
  }); */


// Handle accept and decline buttons (simulated)
/* document.addEventListener('click', function (event) {
  if (event.target.classList.contains('btn-accept') || event.target.classList.contains('btn-decline')) {
    // Simulate backend logic for accepting or declining the invitation

    // Update message
      document.getElementById('message').innerText = event.target.classList.contains('btn-accept') ?
      'Your invitation has been accepted' :
      'Your invitation has been declined';

    // Hide accept and decline buttons show start button
    event.target.closest('tr').querySelector('.action-col').innerHTML = '<button class="btn btn-success start-btn">Start</button>';
  }
});
 */
// Handle start button click and toggle checkmark
document.addEventListener('click', function (event) {
  if (event.target.classList.contains('start-btn')) {
    const checkMark = '<span class="text-success">&#10003;</span>';
    const buttonText = event.target.innerHTML;

    if (buttonText.includes(checkMark)) {
      // Call startRequest function
      startRequest(my.username, my.opponent_username);
      // Update message
      document.getElementById('message').innerText = 'Start request sent';

      // Remove checkmark
      event.target.innerHTML = 'Start';
    } else {
      // Add checkmark
      event.target.innerHTML = `${checkMark} Start`;
    }
  }
});

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
/* inviteButton.onclick = function () {
    invitationMessage.style.display = 'block';
    invite();
} */

function invite(username) {
    // Get necessary data and call socket.sendJSON
    //username = inviteInput.value;
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
var voteCount = -1;
// Vote count ll be 1 at start if 
function startRequest(player1, player2) {
    voteCount *= -1;
    socket.sendJSON({
        action: 'start.request',
        game_id: my.game_id,
        player1: player1,
        player2: player2,
        vote: voteCount,
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
function gameEnded() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'end',
        game_id: 'game_id',
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










