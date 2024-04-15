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
      unblocked: "अनब्लॉक किया गया है",
      followed: "को फॉलो किया गया है",
      unfollowed: "का अनुसरण किया गया है",
      blockedfollow: "ब्लॉक किया गया है आप उसे फॉलो नहीं कर सकते",
      inviteyou: "आपने एक निमंत्रण भेजा है",
      invitehe: "आपने एक निमंत्रण प्राप्त किया है",
      acceptyou: "आपका निमंत्रण स्वीकृत हुआ",
      accepthe: "आपने निमंत्रण स्वीकार किया",
      declineyou: "आपका निमंत्रण अस्वीकृत हुआ",
      declinehe: "आपने निमंत्रण अस्वीकार किया",
  },
  pt: {
      blocked: "foi bloqueado",
      unblocked: "foi desbloqueado",
      followed: "foi seguido",
      unfollowed: "deixou de seguir",
      blockedfollow: "foi bloqueado você não pode segui-lo",
      inviteyou: "Você enviou um convite",
      invitehe: "Você recebeu um convite",
      acceptyou: "Seu convite foi aceito",
      accepthe: "Você aceitou o convite",
      declineyou: "Seu convite foi recusado",
      declinehe: "Você recusou o convite",
  },
  en: {
      blocked: "has been blocked",
      unblocked: "has been unblocked",
      followed: "has been followed",
      unfollowed: "has been unfollowed",
      blockedfollow: "has been blocked you can't follow him/her",
      inviteyou: "You sent an invitation",
      invitehe: "You received an invitation",
      acceptyou: "Your invitation accepted",
      accepthe: "You accepted invitation",
      declineyou: "Your invitation declined",
      declinehe: "You declined invitation",
     
  },
  tr: {
      blocked: "engellendi",
      unblocked: "engeli kaldırıldı",
      followed: "takip edildi",
      unfollowed: "takipten çıkarıldı",
      blockedfollow: "engellendi takip edemezsiniz",
      inviteyou: "Davet gönderdiniz",
      invitehe: "Davet aldınız",
      acceptyou: "Davetiniz kabul edildi",
      accepthe: "Davet kabul edildi",
      declineyou: "Davetiniz reddedildi",
      declinehe: "Davet reddedildi",
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
  const acceptButton = document.getElementById("accept");
  const declineButton = document.getElementById("decline");
  const unblockButton = document.getElementById("unblock");
  const followButton = document.getElementById("follow");
  const unfollowButton = document.getElementById("unfollow");
  const messages = document.getElementById("messages");

  const chatsocket = new WebSocket("wss://" + window.location.host + "/ws/chat/" + roomName + "/")

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

document.addEventListener('click', function(e) {
  if (e.target.tagName === 'A' && e.target.hasAttribute('data-url')) {
    var url = e.target.getAttribute('data-url');
    if (url.includes('/remote-game/tournament/')) {
      e.preventDefault();
      swapApp(url);
    }
  }
});

  chatsocket.onmessage = function (e) {
      const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
      const lang = cookie ? cookie.split('=')[1] : 'en';
      const data = JSON.parse(e.data)
      
      
      switch (data.type) {
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
        case 'invite.game':
          if (user === data.inviter) {
            showToast(`${langMessages[lang]['inviteyou']}`, 'text-bg-info', 'bi bi-bug-fill');
          } else {
            showToast(`${langMessages[lang]['invitehe']}`, 'text-bg-info', 'bi bi-bug-fill');
            acceptButton.style.display = 'block';
            declineButton.style.display = 'block';
          }
          break;
        case 'accept.game':
          if (user === data.accepted) {
            showToast(`${langMessages[lang]['acceptyou']}`, 'text-bg-success', 'bi bi-bug-fill');
          } else {
            showToast(`${langMessages[lang]['accepthe']}`, 'text-bg-success', 'bi bi-bug-fill');
            acceptButton.style.display = 'none';
            declineButton.style.display = 'none';
          }
          swapApp(`/remote-game/invite/${data.game_id}`);
          break;

        case 'decline.game':
          if (user === data.declined) {
            showToast(`${langMessages[lang]['declineyou']}`, 'text-bg-success', 'bi bi-bug-fill');
          } else {
            showToast(`${langMessages[lang]['declinehe']}`, 'text-bg-success', 'bi bi-bug-fill');
          }
          break;

        case 'blocked':
          if (data.blocker === user) {
            unblockButton.style.display = 'block';
            blockButton.style.display = 'none';
            sendButton.disabled = true;
            sendButton.style.color = 'red';
            conversation.style.display = 'none';
            showToast(`${data.blocked} ${langMessages[lang][data.type]}`, 'text-bg-danger', 'bi bi-bug-fill');
          }
          break;
        case 'unblocked':
          if (data.unblocker === user) {
            unblockButton.style.display = 'none';
            blockButton.style.display = 'block';
            sendButton.style.color = '#94a3b8';
            sendButton.disabled = false;
            conversation.style.display = 'block';
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
    console.log(userNameOnChat + ' clicked');
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
    //console.log("invite button clicked");
    chatsocket.send(JSON.stringify({
      "action": "invite.game",
  }))
  }

  acceptButton.onclick = function (e) {
    chatsocket.send(JSON.stringify({
      "action": "accept.game",
      "accepted": userNameOnChat,
      "accepter": user,
    }))
  }

  declineButton.onclick = function (e) {
    chatsocket.send(JSON.stringify({
      "action": "decline.game",
    }))
  }

  followButton.onclick = function (e) {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
    const lang = cookie ? cookie.split('=')[1] : 'en';
    if (unblockButton.style.display === 'block') {
      showToast(`${userNameOnChat} ${langMessages[lang].blockedfollow}`, 'text-bg-danger', 'bi bi-bug-fill');
      return;
    }
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    fetch(`/follow_unfollow/${userNameOnChat}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ action: "follow" })
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 'ok') {
            showToast(`${userNameOnChat} ${langMessages[lang].followed}`, 'text-bg-success', 'bi bi-bug-fill');
            followButton.style.display = 'none';
            unfollowButton.style.display = 'block';
      }
    });
  }

  unfollowButton.addEventListener('click', function(e) {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
    const lang = cookie ? cookie.split('=')[1] : 'en';

    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    fetch(`/follow_unfollow/${userNameOnChat}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ action: "unfollow" })
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 'ok') {
            showToast(`${userNameOnChat} ${langMessages[lang].unfollowed}`, 'text-bg-danger', 'bi bi-bug-fill');
            unfollowButton.style.display = 'none';
            followButton.style.display = 'block';
        }
      });
    });

}
