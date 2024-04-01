import { initializeBurger } from './burger.js';
import { initializeLogin, makeLogin } from './login.js';
import { initializeSignup, makeRegister } from './signup.js';
import { initializeProfile, toggleGame, matchHistoryChanger} from './profile.js';
import { initializeSearch } from './search.js';
import { initializeStore } from './store.js';
import { initializeInventory } from './inventory.js';
import { editProfile, editPassword, editSocial, deleteAccount, changeAvatar, displaySection } from './profile-settings.js';
import { getChat } from './base-chat.js'
import { innerChat } from './chat.js';

function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

const fill = document.querySelector('.progress-bar-fill');

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
    var title = 'IndianPong';
  }

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
window.initializeLogin = initializeLogin;
window.initializeSignup = initializeSignup;
window.makeLogin = makeLogin;
window.makeRegister = makeRegister;
window.initializeProfile = initializeProfile;
window.toggleGame = toggleGame;
window.matchHistoryChanger = matchHistoryChanger;
window.initializeSearch = initializeSearch;
window.initializeStore = initializeStore;
window.initializeInventory = initializeInventory;
window.editProfile = editProfile;
window.editPassword = editPassword;
window.editSocial = editSocial;
window.deleteAccount = deleteAccount;
window.changeAvatar = changeAvatar;
window.displaySection = displaySection;
window.getChat = getChat;
window.innerChat = innerChat;

window.onpopstate = function(event) {
  if (window.location.hash == '') // Eğer # ile başlayan bir path değilse değişim yaptırıyoruz çünkü profile-settings alanında # ile başlayan path yönlendirmeleri var onlarla çakışıp yönlendirmeyi engelliyor.
    updateApp(window.location.pathname);
};

function pageHandler(path) {
    const pathParts = path.split('/');
    console.log(pathParts + ' ' + pathParts.length);
    if (path.includes('/login'))
      initializeLogin();
    else if (path.includes('/signup'))
      initializeSignup();
    else if(path.includes('/settings'))
    {
      
    }
    else if(path.includes('/profile/'))
      initializeProfile();
    else if(path.includes('/search'))
      initializeSearch();
    else if(path.includes('/store/'))
      initializeStore();
    else if(path.includes('/inventory/'))
      initializeInventory();
    else if (pathParts[1] === 'chat' && pathParts.length === 3) {
      console.log('chat1');
      getChat();
    }
    else if (pathParts[1] === 'chat' && pathParts.length === 4) {
      console.log('chat');
      innerChat();
    }
    if (path != '/' && path != '/login' && path != '/signup')
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