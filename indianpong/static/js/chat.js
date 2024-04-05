export function innerChat() {

function showToast(content, status, iconClass) {
  const liveToast = document.getElementById('liveToast');
  var toastContent = document.querySelector('#liveToast .fw-semibold');
  var toastIcon = document.querySelector('.toast-body .i-class i');

  toastIcon.className = iconClass;
  liveToast.classList.remove('text-bg-danger'); 
  liveToast.className = 'toast'; 
  liveToast.classList.add(status);

  toastContent.textContent = content;
  const toast = new bootstrap.Toast(liveToast);
  toast.show();
  setTimeout(function() {
      toast.hide();
  }, 8000);
}

const langMessages = {
  hi: {
      blocked: "ब्लॉक किया गया है",
      unblocked: "अनब्लॉक किया गया है"
  },
  pt: {
      blocked: "foi bloqueado",
      unblocked: "foi desbloqueado"
  },
  en: {
      blocked: "has been blocked",
      unblocked: "has been unblocked"
  },
  tr: {
      blocked: "engellendi",
      unblocked: "engeli kaldırıldı"
  }
};

  const roomName = JSON.parse(document.getElementById("room-name").textContent);
  const user = JSON.parse(document.getElementById("user").textContent);
  const sendButton = document.getElementById("send");
  const conversation = document.getElementById("conversation");
  const inputField = document.getElementById("comment");
  const userNameOnChat = document.getElementById("userNameOnChat").textContent.trim();
  const blockButton = document.getElementById("block");
  const inviteButton = document.getElementById("invite");
  const unblockButton = document.getElementById("unblock");
  const messages = document.getElementById("messages");

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

  function messageMe(data){
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
    return message
  }

  function messageOthers(data) {
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
    return message
  }


  chatsocket.onmessage = function (e) {
      const lang = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage=')).split('=')[1];
      const data = JSON.parse(e.data)
      switch (data.type) {
/*         case 'blocked':
          console.log('blocked') */
        case 'chat.message':
          if (user === data.user) {
            var message = messageMe(data);
          } else {
            var message = messageOthers(data);
          }
          conversation.innerHTML += message
          setTimeout(() => {
            conversation.scrollTop = conversation.scrollHeight;
          }, 0);
          break;
        case 'accept':
          if (user === data.accepted) {
            showToast(`Your invitation accepted`, 'text-bg-success', 'bi bi-bug-fill');
          } else {
            showToast(`You accepted invitation`, 'text-bg-success', 'bi bi-bug-fill');
          }
          swapApp(`/remote-game/invite/${data.game_id}`);
          break;

        case 'decline':
          if (user === data.declined) {
            showToast(`Your invitation declined`, 'text-bg-danger', 'bi bi-bug-fill');
          } else {
            showToast(`You declined invitation`, 'text-bg-danger', 'bi bi-bug-fill');
          }
          break;

        case 'blocked':
          if (data.blocker === user) {
            unblockButton.style.display = 'block';
            blockButton.style.display = 'none';
            sendButton.disabled = true;
            messages.style.display = 'none';
            showToast(`${data.blocked} ${langMessages[lang][data.type]}`, 'text-bg-danger', 'bi bi-bug-fill');
          }
          break;
        case 'unblocked':
          if (data.unblocker === user) {
            unblockButton.style.display = 'none';
            blockButton.style.display = 'block';
            sendButton.disabled = false;
            messages.style.display = 'block';
            showToast(`${data.unblocked} ${langMessages[lang][data.type]}`, 'text-bg-success', 'bi bi-bug-fill');
          }
          break;
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
      console.log(userNameOnChat)
      chatsocket.send(JSON.stringify({
          "action": "chat",
          "user": user, 
          "message": message,
      }))
      inputField.value = ''
  }

  blockButton.onclick = function (e) {
    console.log(userNameOnChat);
    chatsocket.send(JSON.stringify({
        "action": "block",
        "blocked": userNameOnChat,
    }))
  }

  unblockButton.onclick = function (e) {
    chatsocket.send(JSON.stringify({
        "action": "unblock",
        "unblocked": userNameOnChat,
    }))
  }

  inviteButton.onclick = function (e) {
    chatsocket.send(JSON.stringify({
      "action": "invite",
      "inviter": user,
      "invited": userNameOnChat,
  }))
  }
}
