export function initializeLogin() {
  const passwordInput = document.getElementById('id_password');
  const toggleButton = document.getElementById('togglePassword');

  toggleButton.addEventListener('mousedown', function() {
    passwordInput.type = 'text';
    toggleButton.classList.remove('bi-eye-slash-fill');
    toggleButton.classList.add('bi-eye-fill');
  });

  toggleButton.addEventListener('mouseup', function() {
    passwordInput.type = 'password';
    toggleButton.classList.remove('bi-eye-fill');
    toggleButton.classList.add('bi-eye-slash-fill');
  });
  passwordInput.addEventListener('input', function() {
    toggleButton.style.display = this.value.trim() !== '' ? 'block' : 'none';
  });
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
  }

export function makeLogin(check) {
  if(!check)
    return;
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