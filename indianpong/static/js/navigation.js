function updateApp(path) {
    fetch(path)
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
            if (path == '/signup')
                initializePage();
        })
        .catch(error => console.error(error));
}

function swapApp(path) {
    currentPath = window.location.pathname;
    window.history.pushState({}, '', path);
       
    updateApp(path);
}

function initializePage() {
    const fileInput = document.getElementById('id_avatar');
    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const selectedLanguage = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage')).split('=')[1];
            var file = this.files[0];
            if (file.size > 2.6 * 1024 * 1024) {
                var messages = {
                    'en': "Photo must be under 2.6MB!",
                    'tr': "Fotoğraf 2.6MB'dan küçük olmalıdır!",
                    'hi': "फोटो 2.6MB से कम होना चाहिए!",
                    'pt': "A foto deve ter menos de 2,6 MB!"
                };
                var message = messages[selectedLanguage] || "Photo must be under 2.6MB!";
                showToast(message, "text-bg-danger", "bi bi-image");
                this.value = '';
            }
            else {
                var messages = {
                    'en': "Photo added!",
                    'tr': "Fotoğraf eklendi!",
                    'hi': "फोटो जोड़ दी गई!",
                    'pt': "Foto adicionada!"
                };
                var message = messages[selectedLanguage] || "Photo added!";
                showToast(message, "text-bg-success", "bi bi-image");
            }
        });
    }

    
}


window.onpopstate = function(event) {
    updateApp(window.location.pathname);
};

function setLanguage(language) {
    document.cookie = "selectedLanguage=" + language;
    swapApp(window.location.pathname);
}

function makeLogin() {
    var form = document.getElementById('loginForm');
    var formData = new FormData(form);

    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

    fetch('/login', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      if (data == "dashboard")
        swapApp('/dashboard');
      else {
        showToast(`${data}`, `text-bg-danger`, `bi bi-bug-fill`);
      }
    })
    .catch(error => {
      console.error(error);
    });
  }
  
function makeRegister() {
    var form = document.getElementById('registerForm');
    var formData = new FormData(form);

    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

    fetch('/signup', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      if (data == "login") {
        swapApp('/login');
      }
      else {
        document.body.innerHTML = data;
      }
      })
    .catch(error => {
      console.error(error);
    });
  }