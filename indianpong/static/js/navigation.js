import { initializeLogin, makeLogin } from './login.js';
import { initializeSignup, makeRegister } from './signup.js';
import { initializeProfile, toggleGame, matchHistoryChanger} from './profile.js';
import { initializeSearch } from './search.js';
import { initializeStore } from './store.js';
import { initializeInventory } from './inventory.js';
import { initializeBurger } from './burger.js';

function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

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
  let title;
  const lang = getCookie('selectedLanguage');
  console.log(path);
  switch (path) {
    case '/':
      title = 'Indian Pong';
      break;
    case '/login':
      title = lang == 'en' ? 'Indian Pong - Login' : lang == 'hi' ? 'इंडियन पोंग - लॉग इन' : lang == 'pt' ? 'Pong Indiano - Login' : lang == 'tr' ? 'Hint Pong - Giriş' : 'Indian Pong - Login';
      break;
    case '/signup':
      title = 'Indian Pong - Signup';
      break;
    case '/settings':
      title = 'Indian Pong - Settings';
      break;
    case '/profile':
      title = 'Indian Pong - Profile';
      break;
    case '/search':
      title = 'Indian Pong - Search';
      break;
    case '/store':
      title = 'Indian Pong - Store';
      break;
    case '/inventory':
      title = 'Indian Pong - Inventory';
      break;
    default:
      title = 'Indian Pong';
  }
  document.title = title;
}

function swapApp(path) {
  //currentPath = window.location.pathname;
  window.history.pushState({}, '', path);
  updateApp(path);
  updateTitle(path);
}

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
window.initializeBurger = initializeBurger;


window.onpopstate = function(event) {
  if (window.location.hash == '') // Eğer # ile başlayan bir path değilse değişim yaptırıyoruz çünkü profile-settings alanında # ile başlayan path yönlendirmeleri var onlarla çakışıp yönlendirmeyi engelliyor.
    updateApp(window.location.pathname);
};

function pageHandler(path) {
    if (path == '/login')
      initializeLogin();
    else if (path == '/signup')
      initializeSignup();
    else if(path.includes('/profile/'))
      initializeProfile();
    else if(path.includes('/search'))
      initializeSearch();
    else if(path.includes('/store/'))
      initializeStore();
    else if(path.includes('/inventory/'))
      initializeInventory();
    
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