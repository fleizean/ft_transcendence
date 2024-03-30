import { initializeLogin, makeLogin } from './login.js';
import { initializeSignup, makeRegister } from './signup.js';

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

function swapApp(path) {
  //currentPath = window.location.pathname;
  window.history.pushState({}, '', path);
  updateApp(path);
}

window.swapApp = swapApp;
window.initializeLogin = initializeLogin;
window.initializeSignup = initializeSignup;
window.makeLogin = makeLogin;
window.makeRegister = makeRegister;

window.onpopstate = function(event) {
  if (window.location.hash == '') // Eğer # ile başlayan bir path değilse değişim yaptırıyoruz çünkü profile-settings alanında # ile başlayan path yönlendirmeleri var onlarla çakışıp yönlendirmeyi engelliyor.
    updateApp(window.location.pathname);
};

function setLanguage(language) {
  document.cookie = "selectedLanguage=" + language;
  swapApp(window.location.pathname);
}



function pageHandler(path) {
    if (path == '/login') {
      initializeLogin();
    }
    else if (path == '/signup') {
      initializeSignup();
    }
}

function showLoadingScreen() {
  document.getElementById('loading-bar').style.width = '100%';;
}

// Yükleme ekranını gizle
function hideLoadingScreen() {
  document.getElementById('loading-bar').style.width = '0';;
}