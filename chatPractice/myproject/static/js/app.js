const roomName = JSON.parse(document.getElementById("room-name").textContent)
const conversation = document.getElementById("conversation")
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")
const sendButton = document.getElementById("send")
const inputField = document.getElementById("comment")

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)
    var message = ` <div class="row message-body">
            <div class="col-sm-12 message-main-sender">
                <div class="sender">
                    <div class="message-text">
                        ${data.message}
                    </div>
                    <span class="message-time pull-right">
                        Bugün
                    </span>
                </div>
            </div>
        </div>`
    conversation.innerHTML += message
};

chatSocket.onclose = function (e) {
    console.error("soket beklenmedik şekilde kapandı!")
}

inputField.focus()
inputField.onkeyup = function (e) {
    if (e.keyCode === 13) {
        sendButton.click()
    }
}

sendButton.onclick = function (e) {
    const message = inputField.value

    chatSocket.send(JSON.stringify({
        "message": message
    }))
    inputField.value = ''
}
