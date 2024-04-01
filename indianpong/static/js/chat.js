export function innerChat() {
  const roomName = JSON.parse(document.getElementById("room-name").textContent)
  const user = JSON.parse(document.getElementById("user").textContent)
  const sendButton = document.getElementById("send");
  const conversation = document.getElementById("conversation")
  const inputField = document.getElementById("comment")


  const chatsocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")

  chatsocket.onopen = function (e) {
      console.log("socket opened")
  }

  chatsocket.onclose = function (e) {
      console.error("socket closed unexpectedly")
  }

  chatsocket.onerror = function (e) {
      console.error("socket error")
  }


  chatsocket.onmessage = function (e) {
      const data = JSON.parse(e.data)
      switch (data.type) {

        case 'chat.message':
          if (user === data.user) {
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
          } else {
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
          }
          conversation.innerHTML += message
          setTimeout(() => {
            conversation.scrollTop = conversation.scrollHeight;
          }, 0);
      };
  }


  inputField.focus()
  inputField.onkeyup = function (e) {
      if (e.keyCode === 13) {
          sendButton.click()
      }
  }


  sendButton.onclick = function (e) {
      const message = inputField.value
      chatsocket.send(JSON.stringify({
          "action": "chat",
          "user": user, 
          "message": message,
      }))
      inputField.value = ''
  }
}