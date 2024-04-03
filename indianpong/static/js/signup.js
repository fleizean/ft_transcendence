export function initializeSignup() {
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

    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

  const fileInput = document.getElementById('id_avatar');
  if (fileInput) {
      fileInput.addEventListener('change', function(event) {
        const selectedLanguage = getCookie('selectedLanguage');
          var file = this.files[0];
          if (file && file.size > 2 * 1024 * 1024) {
              var messages = {
                  'en': "Photo must be under 2MB!",
                  'tr': "Fotoğraf 2MB'dan küçük olmalıdır!",
                  'hi': "फोटो 2MB से कम होना चाहिए!",
                  'pt': "A foto deve ter menos de 2MB!"
              };
              var message = messages[selectedLanguage] || "Photo must be under 2MB!";
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

export function makeRegister(check) {
  if (!check)
    return;
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
      } else {
        document.body.innerHTML = data;
      }
    })
    .catch(error => {
      console.error(error);
    });
}

