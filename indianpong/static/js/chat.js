const roomName = JSON.parse(document.getElementById("room-name").textContent)
const user = JSON.parse(document.getElementById("user").textContent)
const conversation = document.getElementById("conversation")
const sendButton = document.getElementById("send")
const inputField = document.getElementById("comment")
const inviteButton = document.getElementById("inviteButton")
const acceptButton = document.getElementById("acceptButton")
const declineButton = document.getElementById("declineButton")
//acceptButton.style.display = 'none';
//declineButton.style.display = 'none';


// const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")
import { socket } from "./gamesocket.js";

socket.onmessage = function (e) {
    const data = JSON.parse(e.data)

    switch (data.type) {
      case 'user.online':
        socket.send(JSON.stringify({
          "action": "room",
          "room_name": roomName,
        }))

        // Show online users
        console.log('Online users:', data.users);

        console.log('Player connected:', data.username);
        //console.log(my.username);
        break;

      case 'user.offline':

        console.log('Player disconnected:', data.username);
        break;

      case 'chat.message':
        if (data.message === `Let's play!`) {
          console.log('Player invited:', data.user);
          console.log(user + " " + opponent);
          if (user !== data.user) {
            // acceptButton.style.display = 'block';
             //declineButton.style.display = 'block';
          }
          if (user === data.user) {
            invite();
          }
        }
        else if (data.message === 'Kabul ediyorum mk') {
          console.log('Player accepted:', data.user);
          console.log(user + " " + opponent);
          if (user !== data.user) {
            acceptGame(opponent + "_" + user, opponent, user);
          }
          // window.location.href = '/game'; // refreshes the page
          //history.pushState({}, '', '/game'); // changes the url without refreshing the page
          // fetch /game and replace inner html within <div class="app" id="app">
          fetch('/game')
          .then(response => response.text())
          .then(html => {
            const appDiv = document.getElementById('app');
            appDiv.innerHTML = html;
          })
          .catch(error => console.error('Error:', error));
        }
        if (data.message === `Let's play!`) {
          console.log('Player invited:', data.user);
          console.log(user + " " + opponent);
          if (user !== data.user) {
            acceptButton.style.display = 'block';
            declineButton.style.display = 'block';
          }
          if (user === data.user) {
            invite();
          }
        }
        else if (data.message === 'Kabul ediyorum mk') {
          console.log('Player accepted:', data.user);
          console.log(user + " " + opponent);
          if (user !== data.user) {
            acceptGame(opponent + "_" + user, opponent, user);
          }
          // Fetch /game and replace inner HTML within <div class="app" id="app">

        }
        else if (data.message === 'İstemiyorum mk') {
          console.log('Player declined:', data.user);
          if (user !== data.user) {
            declineGame(opponent + "_" + user, opponent, user);
          }
        }
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

socket.sendJSON = function (data) {
  socket.send(JSON.stringify(data));
}

// Splite roomName to get username
var roomNameArray = roomName.split('_');
// Take the one which is not user
var opponent = roomNameArray[0] === user ? roomNameArray[1] : roomNameArray[0];

function invite() {
  // Get necessary data and call socket.sendJSON
  //username = inviteInput.value;
  // maybe put in action.js
  socket.sendJSON({
      action: 'invite',
      invited: opponent,
  });
}



socket.onclose = function (e) {
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
    socket.send(JSON.stringify({
        "action": "message",
        "user": user, 
        "message": message,
    }))
    inputField.value = ''
}


inviteButton.onclick = function (e) {
  const message = `Let's play!`

  socket.send(JSON.stringify({
    "action": "message",
    "user": user, 
    "message": message,
      }))
      inputField.value = ''
      // Delay 2 seconds
      //setTimeout(redirect, 2000);
      // Redirect to /game

  }
  
  acceptButton.onclick = function (e) {
    accept()
  }
  declineButton.onclick = function (e) {
    decline()
  }

  function accept() {
    const message = `Kabul ediyorum mk`
    socket.send(JSON.stringify({
      "action": "message",
      "user": user, 
      "message": message,
  }))
  inputField.value = ''
  }
  
  function decline() {
    const message = `İstemiyorum mk`
    socket.send(JSON.stringify({
      "action": "message",
      "user": user, 
      "message": message,
  }))
  inputField.value = ''
  declineGame(roomName, opponent, user);
  }

  function acceptGame(group_name, inviter, invited) {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'accept',
        group_name: group_name,
        accepted: inviter,
        accepter: invited,
    });
}

function declineGame(group_name, inviter, invited) {
    // Get necessary data and call socket.sendJSON
    socket.sendJSON({
        action: 'decline',
        group_name: group_name,
        declined: inviter,
        decliner : invited,
    });
}