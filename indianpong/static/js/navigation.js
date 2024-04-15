import { initializeBurger } from './burger.js';
import { getChat } from './base-chat.js'
import { innerChat } from './chat.js';
import { makeRegister, initializeSignup } from './signup.js';
import { makeLogin, initializeLogin } from './login.js';
import { editProfile, editPassword, editSocial, deleteAccount, changeAvatar, displaySection, unblockButon } from './profile-settings.js';
import { matchHistoryChanger, toggleGame, followButton, unfollowButton } from './profile.js';
import { Game } from './game/play-ai.js';
import { LocalGame } from './game/local-game.js';
import { localTournament } from './game/localTournament.js';
import { Rps } from './rps.js';
import { RemotePong } from './game/sockPong.js';
import { RemoteRps } from './sockRps.js';
import { createTournament } from './create-tournament.js';
import { initializeSearch, makeSearch } from './search.js';
import { displaySectionGame, joinTournament, leaveTournament, startTournament, showToast } from './tournament-room.js';

export function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

const fill = document.querySelector('.progress-bar-fill');

document.addEventListener('DOMContentLoaded', function() {
  updateApp(window.location.pathname);
});

function updateApp(path) {
  showLoadingScreen();
  fetch(path)
    .then(response => response.text())
    .then(html => {
      document.body.innerHTML = html;
      pageHandler(path);
      hideLoadingScreen();
    })
    .catch(error => console.error(error));
}

function updateTitle(path) {
  // Split the path by slashes
  var parts = path.split('/');

  if (parts.length > 0) {
    // Remove the first empty string from the parts array
    parts.shift();

    // Map over each part to capitalize the first letter
    var titleParts = parts.map(function(part) {
      return part.charAt(0).toUpperCase() + part.slice(1);
    });

    // Join the title parts with spaces
    var title = titleParts.join(' ');
  }
  else {
    // If there are no parts, set the title to 'Home'
    var title = 'Indian-Pong';
  }

  if (!title)
    title = 'Indian-Pong';
  // Set the document title
  document.title = title;
}

function swapApp(path) {
  //currentPath = window.location.pathname;
  window.history.pushState({}, '', path);
  updateApp(path);
  updateTitle(path);
}

window.initializeBurger = initializeBurger;
window.swapApp = swapApp;
window.getChat = getChat;
window.innerChat = innerChat;
window.makeRegister = makeRegister;
window.initializeSignup = initializeSignup;
window.makeLogin = makeLogin;
window.initializeLogin = initializeLogin;
window.editProfile = editProfile;
window.editPassword = editPassword;
window.editSocial = editSocial;
window.deleteAccount = deleteAccount;
window.changeAvatar = changeAvatar;
window.displaySection = displaySection;
window.matchHistoryChanger = matchHistoryChanger;
window.toggleGame = toggleGame;
window.followButton = followButton;
window.unfollowButton = unfollowButton;
window.Game = Game;
window.LocalGame = LocalGame;
window.localTournament = localTournament;
window.Rps = Rps;
window.createTournament = createTournament;
window.unblockButon = unblockButon;
window.RemotePong = RemotePong;
window.RemoteRps = RemoteRps;
window.initializeSearch = initializeSearch;
window.makeSearch = makeSearch;
window.displaySectionGame = displaySectionGame;
window.startTournament = startTournament;
window.joinTournament = joinTournament;
window.leaveTournament = leaveTournament;

window.onpopstate = function(event) {
  if (window.location.hash == '') {
    updateApp(window.location.pathname);
  }
};


function pageHandler(path) {
    const pathParts = path.split('/');
    getCookie();
    if (animationId)
      cancelAnimationFrame(animationId);
    if (localTournamentAnimationId)
      cancelAnimationFrame(localTournamentAnimationId);
    if (localGameAnimationId)
      cancelAnimationFrame(localGameAnimationId);

    if (path.includes('/login')) {
      makeLogin();
      initializeLogin();
    }
    else if (path.includes('/signup')) {
      makeRegister();
      initializeSignup();
    }
    else if(path.includes('/settings')) {
      editProfile();
      editPassword();
      editSocial();
      deleteAccount();
      changeAvatar();
      displaySection();
      unblockButon();
    }
    else if(path.includes('/profile/')) {
      matchHistoryChanger();
      toggleGame();
      followButton();
      unfollowButton();
    }
    else if (path.includes('/friends/')) {
      getChat();
    }
    else if(path.includes('/search')) {
      //addScript('search');
      initializeSearch();
      makeSearch();
    }
    else if(path.includes('/store/')) {
      //addScript('store');
      const script = document.createElement('script');
      script.src = '/static/js/store.js';
      document.body.appendChild(script);
    }
    else if(path.includes('/inventory/')) {
      //addScript('inventory');
      const script = document.createElement('script');
      script.src = '/static/js/inventory.js';
      document.body.appendChild(script);
    }
    else if (pathParts[1] === 'chat' && pathParts.length === 3) {
      getChat();
    }
    else if (pathParts[1] === 'chat' && pathParts.length === 4) {
      innerChat();
    }
    else if (path.includes('/play-ai/')) {
      Game();
    }
    else if (path.includes('/local-game')) {
      LocalGame();
    }
    else if (path.includes('/local-tournament')) {
      localTournament();
    }
    else if (path.includes('/play-rps-ai')) {
      Rps();
    }
    else if (path.includes('/remote-game/')) {
      RemotePong();
    }
    else if (path.includes('/play-rps')) {
      RemoteRps();
    }
    else if (path.includes('/tournament-room/')) {
      displaySectionGame();
      startTournament();
      joinTournament();
      leaveTournament();
      showToast();
    }

    if (path != '/' && path != '/login' && path != '/signup' && !path.includes('set_password') && path != '/password_reset')
      initializeBurger();
}

function showLoadingScreen() {
  document.getElementById('loading-bar').style.width = '100%';;
}

// Yükleme ekranını gizle
function hideLoadingScreen() {
  document.getElementById('loading-bar').style.width = '0';;
}

/* function showProgressBar() {
  document.querySelector('.progress-bar').style.display = 'block';
}

function hideProgressBar() {
  document.querySelector('.progress-bar').style.display = 'none';
} */

