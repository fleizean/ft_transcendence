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

export function makeRegister(check) {
  if (!check)
    return;
  const selectedLanguage = getCookie('selectedLanguage');
  if (document.getElementById('gdprCheckbox').checked == false) {
    if (selectedLanguage == 'en')
      showToast("Please accept the terms and conditions", "text-bg-danger", "bi bi-exclamation-triangle-fill");
    else if (selectedLanguage == 'tr')
      showToast("Lütfen şartları ve koşulları kabul edin", "text-bg-danger", "bi bi-exclamation-triangle-fill");
    else if (selectedLanguage == 'hi')
      showToast("कृपया नियम और शर्तों को स्वीकार करें", "text-bg-danger", "bi bi-exclamation-triangle-fill");
    else if (selectedLanguage == 'pt')
      showToast("Por favor, aceite os termos e condições", "text-bg-danger", "bi bi-exclamation-triangle-fill");
    return;
  }
  var form = document.getElementById('registerForm');
  var formData = new FormData(form);
  var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

  if (formData.get['username'] == 'IndianAI') {
    if (selectedLanguage == 'en')
      showToast("Username is not allowed", "text-bg-danger", "bi bi-person-x-fill");
    else if (selectedLanguage == 'tr')
      showToast("Kullanıcı adı izin verilmiyor", "text-bg-danger", "bi bi-person-x-fill");
    else if (selectedLanguage == 'hi')
      showToast("उपयोगकर्ता नाम अनुमत नहीं है", "text-bg-danger", "bi bi-person-x-fill");
    else if (selectedLanguage == 'pt')
      showToast("Nome de usuário não permitido", "text-bg-danger", "bi bi-person-x-fill");  
  }
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

