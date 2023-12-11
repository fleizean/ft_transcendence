
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    displayMessage(data.message);
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

function sendMessage(message) {
    chatSocket.send(JSON.stringify({ 'message': message }));
}
