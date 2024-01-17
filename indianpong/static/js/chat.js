const roomName = JSON.parse(document.getElementById("room-name").textContent)
const user = JSON.parse(document.getElementById("user").textContent)
const conversation = document.getElementById("conversation")
const sendButton = document.getElementById("send")
const inputField = document.getElementById("comment")


const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)

    if(user === data.user){

        
             var message = `
        <li class="conversation-item">
            <div class="conversation-item-content">
              <div class="conversation-item-wrapper">
                <div class="conversation-item-box">
                  <div class="conversation-item-text">
                    <p>${data.message}</p>
                    <div class="conversation-item-time">${data.created_date}</div>
                  </div>
                </div>
              </div>
            </div>
        </li>`
/*          var message = ` <div class="row message-body">
            <div class="col-sm-12 message-main-sender">
                <div class="sender">
                    <div class="message-text">
                        ${data.message}
                    </div>
                    <span class="message-time pull-right">
                        ${data.created_date}
                    </span>
                    </div>
                </div>
            </div>` */
    }else{
       var message = `                  
            <li class="conversation-item me">
              <div class="conversation-item-content">
                <div class="conversation-item-wrapper">
                  <div class="conversation-item-box">
                  </div>
                </div>
                <div class="conversation-item-wrapper">
                  <div class="conversation-item-box">
                    <div class="conversation-item-text">
                    ${data.message}
                      <div class="conversation-item-time">${data.created_date}</div>
                    </div>
                  </div>
                </div>
              </div>
            </li>`
        /* var message = ` <div class="row message-body">
        <div class="col-sm-12 message-main-receiver">
            <div class="receiver">
                <div class="message-text">
                    ${data.message}
                </div>
                <span class="message-time pull-right">
                    ${data.created_date}
                </span>
                </div>
            </div>
        </div>` */
    }
   
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

function showOptions() {
    var optionsDiv = document.getElementById('options');
    if (optionsDiv.style.display === 'none' || optionsDiv.style.display === '') {
        optionsDiv.style.display = 'block';
    } else {
        optionsDiv.style.display = 'none';
    }
}


sendButton.onclick = function (e) {
    const message = inputField.value
    chatSocket.send(JSON.stringify({
        "user": user, 
        "message": message,
    }))
    inputField.value = ''
}
