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

    const passwordInput1 = document.getElementById('id_password1');
    const passwordInput2 = document.getElementById('id_password2');
    const toggleButton1 = document.getElementById('togglePassword1');
    const toggleButton2 = document.getElementById('togglePassword2');
    
    toggleButton1.addEventListener('mousedown', function() {
        passwordInput1.type = 'text';
        toggleButton1.classList.remove('bi-eye-slash-fill');
        toggleButton1.classList.add('bi-eye-fill');
    });
    
    toggleButton1.addEventListener('mouseup', function() {
        passwordInput1.type = 'password';
        toggleButton1.classList.remove('bi-eye-fill');
        toggleButton1.classList.add('bi-eye-slash-fill');
    });
  
    toggleButton2.addEventListener('mousedown', function() {
        passwordInput2.type = 'text';
        toggleButton2.classList.remove('bi-eye-slash-fill');
        toggleButton2.classList.add('bi-eye-fill');
    });
  
    toggleButton2.addEventListener('mouseup', function() {
        passwordInput2.type = 'password';
        toggleButton2.classList.remove('bi-eye-fill');
        toggleButton2.classList.add('bi-eye-slash-fill');
    });
  
    passwordInput1.addEventListener('input', function() {
      toggleButton1.style.display = this.value.trim() !== '' ? 'block' : 'none';
    });
  
    passwordInput2.addEventListener('input', function() {
      toggleButton2.style.display = this.value.trim() !== '' ? 'block' : 'none';
    });
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