import { initializeBurger } from './burger.js';
import { getChat } from './base-chat.js'
import { innerChat } from './chat.js';

function getCookie(name) {
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
window.getChat = getChat;
window.innerChat = innerChat;

window.onpopstate = function(event) {
  if (window.location.hash == '') // Eğer # ile başlayan bir path değilse değişim yaptırıyoruz çünkü profile-settings alanında # ile başlayan path yönlendirmeleri var onlarla çakışıp yönlendirmeyi engelliyor.
    updateApp(window.location.pathname);
  
};

function addScript(pathway) {
  const script = document.createElement('script');
  script.src = '/static/js/' + pathway + '.js';
  document.body.appendChild(script);
}

function pageHandler(path) {
    const pathParts = path.split('/');

    if (path.includes('/login')) {
      //addScript('login');
      const script = document.createElement('script');
      script.src = '/static/js/login.js';
      document.body.appendChild(script);
    }
    else if (path.includes('/signup')) {
      //addScript('signup');
      const script = document.createElement('script');
      script.src = '/static/js/signup.js';
      document.body.appendChild(script);
    }
    else if(path.includes('/settings')) {
      //addScript('profile-settings');
      const script = document.createElement('script');
      script.src = '/static/js/profile-settings.js';
      document.body.appendChild(script);
    }
    else if(path.includes('/profile/')) {
      //addScript('profile');
      const script = document.createElement('script');
      script.src = '/static/js/profile.js';
      document.body.appendChild(script);
    }
    else if(path.includes('/search')) {
      //addScript('search');
      const script = document.createElement('script');
      script.src = '/static/js/search.js';
      document.body.appendChild(script);
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
    else if (path.includes('/play-ai/'))
    {
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