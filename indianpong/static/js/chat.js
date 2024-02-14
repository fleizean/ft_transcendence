const roomName = JSON.parse(document.getElementById("room-name").textContent)
const user = JSON.parse(document.getElementById("user").textContent)
const conversation = document.getElementById("conversation")
const sendButton = document.getElementById("send")
const inputField = document.getElementById("comment")
const inviteButton = document.getElementById("inviteButton")
const userNameOnChat =document.getElementById("userNameOnChat")



const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)

    if(user === data.user){

        
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
    }else{var message = `
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
    }
   
    conversation.innerHTML += message
    setTimeout(() => {
      conversation.scrollTop = conversation.scrollHeight;
    }, 0);
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

inviteButton.onclick = function (e) {
    const message = `<li class="conversation-item">
    <div class="conversation-item-content">
      <div class="conversation-item-wrapper">
        <div class="conversation-item-box">
          <div class="conversation-item-text">
            <p><button id="acceptButton" onclick="window.location.href='/game'">Accept</button>
            <button id="declineButton" onclick=decline()>Decline</button></p>
            <div class="conversation-item-time">111111</div>
          </div>
        </div>
      </div>
    </div>
  </li>`
    chatSocket.send(JSON.stringify({
        "user": user, 
        "message": message,
    }))
    inputField.value = ''
    // Delay 2 seconds
    //setTimeout(redirect, 2000);
    // Redirect to /game
    window.location.href = '/game';
}

function decline() {
  const message = `İstemiyorum mk`
  chatSocket.send(JSON.stringify({
    "user": user, 
    "message": message,
  }))
  inputField.value = ''
}

userNameOnChat.onclick = function(e){
  var username = userNameOnChat.getAttribute("data-username");
  var secondUser = userNameOnChat.getAttribute("data-seconduser");
  if( user === username)
    window.location.href = "/profile/" + secondUser
  else
    window.location.href = "/profile/" + username
}