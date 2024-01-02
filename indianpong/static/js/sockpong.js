// sockpong.js
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');  // Replace with your WebSocket endpoint


const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

socket.onopen = function (e) {
    console.log('WebSocket connection established');
}

socket.onclose = function (e) {
    console.error('WebSocket connection closed');
}

socket.onerror = function (e) {
    console.error('WebSocket error');
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    switch (data.type) {
        case 'user.online':
            console.log('Player connected:', data.username);
            break;
        case 'user.offline':
            console.log('Player disconnected:', data.username);
            break;
        
        case 'game.invite':
            console.log(`Invited Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;
        case 'game.start':
            console.log(`Started Game Id: ${data.game_id} => ${data.player1} vs ${data.player2}`);
            break;
        case 'game.move':
            console.log(`Moving Game Id: ${data.game_id} for ${data.player}: ${data.x} ${data.y}`);
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


function invite() {
    // Get necessary data and call socket.sendJSON
    // maybe put in action.js
    socket.sendJSON({
        action: 'invite',
        opponent: 'opponent_username', // When invite clicked take username somehow
    });
}

function accept() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'accept',
        game_id: 'game_id', // When accept clicked take game_id somehow
    });
}

// send this in setInterval(update, 16) this ll be game state
function move() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'move',
        game_id: 'game_id',
        x: 1, // if this for paddle only y required and for ball both
        y: -1,
        player: 'username', // player1 or player2
    });
}

function endGame() {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'end',
        game_id: 'game_id',
        winner: 'username', // player1 or player2
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

function start() {
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










