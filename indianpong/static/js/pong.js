// pong.js
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');  // Replace with your WebSocket endpoint


const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

const paddleWidth = 10;
const paddleHeight = 60;

const ballSize = 10;

// Initial positions for paddles and ball
let playerPaddleY = canvas.height / 2 - paddleHeight / 2;
let opponentPaddleY = canvas.height / 2 - paddleHeight / 2;
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;

// Handle WebSocket connection opened
socket.addEventListener('open', (event) => {
    console.log('WebSocket connection opened:', event);
});

// Handle messages from the server
socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
        case 'connect':
            console.log('Player connected:', data.player_id);
            break;

        case 'player_disconnect':
            console.log('Player disconnected:', data.player_id);
            break;

        case 'player_update':
            console.log('Player updated:', data.player_id);
            break;

        case 'paddle_update':
            console.log('Paddle updated for player', data.player_id, 'New position:', data.position);
            updatePaddlePosition(data.player_id, data.position);
/*             if (data.player_id === 'player1') {
                playerPaddleY = data.position;
            } else {
                opponentPaddleY = data.position;
            } */
            break;

        case 'ball_update':
            console.log('Ball updated:', data.ball);
            updateBallPosition(data.ball);
/*             ballX = data.ball.x;
            ballY = data.ball.y;   */
            break;

        default:
            console.warn('Unknown message type:', data.type);
    }
});

// Handle paddle movement
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
        // Move paddle up
        const newPosition = playerPaddleY - 10; // Adjust the value as needed
        updatePaddlePosition('player1', newPosition);
        socket.send(JSON.stringify({
            type: 'paddle_update',
            player_id: 'player1',
            position: newPosition,
        }));
    } else if (event.key === 'ArrowDown') {
        // Move paddle down
        const newPosition = playerPaddleY + 10; // Adjust the value as needed
        updatePaddlePosition('player1', newPosition);
        socket.send(JSON.stringify({
            type: 'paddle_update',
            player_id: 'player1',
            position: newPosition,
        }));
    }
});
document.addEventListener('keydown', (event) => {
    if (event.key === 'w') {
        // Move paddle up
        const newPosition = playerPaddleY - 10; // Adjust the value as needed
        updatePaddlePosition('player2', newPosition);
        socket.send(JSON.stringify({
            type: 'paddle_update',
            player_id: 'player2',
            position: newPosition,
        }));
    } else if (event.key === 's') {
        // Move paddle down
        const newPosition = playerPaddleY + 10; // Adjust the value as needed
        updatePaddlePosition('player2', newPosition);
        socket.send(JSON.stringify({
            type: 'paddle_update',
            player_id: 'player2',
            position: newPosition,
        }));
    }
});

// Handle WebSocket connection closed
socket.addEventListener('close', (event) => {
    console.log('WebSocket connection closed:', event);
});

// Handle errors
socket.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});

function updatePaddlePosition(playerId, position) {
    const paddle = document.getElementById(`paddle-${playerId}`);
    
    if (playerId === 'player1') {
        // Update paddle position for player 1
        paddle.style.top = `${position}px`;
    } else if (playerId === 'player2') {
        // Update paddle position for player 2
        paddle.style.bottom = `${position}px`;
    } else {
        // Handle other player IDs or error cases
        console.warn('Unknown player ID:', playerId);
    }
}

function updateBallPosition(ball) {
    const ballElement = document.getElementById('ball');
    ballElement.style.left = `${ball.x}px`;
    ballElement.style.top = `${ball.y}px`;
}

// Handle drawing the paddles and ball on the canvas
function drawPaddles() {
    // Draw player paddle
    context.fillStyle = '#000';
    context.fillRect(0, playerPaddleY, paddleWidth, paddleHeight);

    // Draw opponent paddle
    context.fillStyle = '#000';
    context.fillRect(canvas.width - paddleWidth, opponentPaddleY, paddleWidth, paddleHeight);
}

function drawBall() {
    // Draw the ball
    context.beginPath();
    context.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
    context.fillStyle = '#000';
    context.fill();
    context.closePath();
}

function draw() {
    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Draw paddles and ball
    drawPaddles();
    drawBall();
}


// Animation loop
function animate() {
    draw();
    requestAnimationFrame(animate);
}

// Start the animation loop
animate();