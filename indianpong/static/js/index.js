function displaySection(sectionId) {
    var sections = ["editProfile", "addSocial", "closeAccount", "changePassword"];

    for (var i = 0; i < sections.length; i++) {
        var section = document.getElementById(sections[i]);
        if (sections[i] === sectionId) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    }
}

function displaySectionGame(sectionId) {
    var sections = ["game-bracket-section", "game-room-section"];
    var buttons = ["checkbracket", "gameroombracket"];

    var button = document.getElementById(buttons[1]);
    var button2 = document.getElementById(buttons[0]);
    for (var i = 0; i < sections.length; i++) {
        var section = document.getElementById(sections[i]);
        if (sections[i] === sectionId) {
            section.style.display = 'block';
            if (sectionId === "game-bracket-section") {
                button.style.display = 'inline';
                button2.style.display = 'none';
            }
            else {
                button.style.display = 'none';
                button2.style.display = 'inline';
            }
        } else {
            section.style.display = 'none';
        }
    }
}

document.addEventListener('input', function(event) {
    if (event.target.classList.contains('numbers-only')) {
        var inputValue = event.target.value;

        // Giriş sadece bir rakam olmalı
        if (!/^[0-9]$/.test(inputValue)) {
            event.target.value = ''; // Geçersiz girişi temizle
            return;
        }

        // Pozitif bir sayı olmalı
        var numberValue = parseInt(inputValue, 10);
        if (isNaN(numberValue) || numberValue < 0) {
            event.target.value = ''; // Geçersiz girişi temizle
        }
    }
});


function activateCreateRoom() {
    var value = document.getElementById("createRoom-popup");
    var overlay = document.getElementBywId("overlay");
    if (value) {
        value.style.display = 'flex';
        overlay.style.display = 'block';

    }
}
 
function closeCreateRoom() {
    var value = document.getElementById("createRoom-popup");
    var overlay = document.getElementById("overlay");
    if (value) {
        value.style.display = 'none';
        overlay.style.display = 'none';
    }
}

const checkboxes = document.querySelectorAll('input[name="gameCheckbox"]');

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function () {
      const checkedCheckbox = document.querySelector('input[name="gameCheckbox"]:checked');

      checkboxes.forEach(cb => {
        if (cb !== checkedCheckbox) {
          cb.disabled = checkedCheckbox !== null;
        }
      });
    });
  });

function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    var buttonIcon = document.querySelector('#' + inputId + '+ .input-group button i');

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        buttonIcon.classList.remove("bi-eye");
        buttonIcon.classList.add("bi-eye-slash");
    } else {
        passwordInput.type = "password";
        buttonIcon.classList.remove("bi-eye-slash");
        buttonIcon.classList.add("bi-eye");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector(".navbar-toggler").addEventListener("click", function () {
        var navbarNav = document.getElementById("navbarNav");
        if (navbarNav.classList.contains("show")) {
            navbarNav.classList.remove("show");
        } else {
            navbarNav.classList.add("show");
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector(".burger-menu").addEventListener("click", function () {
        var navLinks = document.querySelector(".nav-links");
        if (navLinks.classList.contains("show")) {
            navLinks.classList.remove("show");
        } else {
            navLinks.classList.add("show");
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('profileNavbar').querySelector(".navbar-toggler").addEventListener("click", function () {
        var profileNavLinks = document.getElementById('profileNavLinks');
        if (profileNavLinks.classList.contains("show")) {
            profileNavLinks.classList.remove("show");
        } else {
            profileNavLinks.classList.add("show");
        }
    });
});


var canvas = document.getElementById("myCanvas");

function setCanvasSize() {
    if (canvas) {
        var maxWidth = window.innerWidth - 370;
        var maxHeight = window.innerHeight - 100;
        console.log("width" + maxWidth)
        console.log("height" + maxHeight)
        // Canvas'ın genişliğini ve yüksekliğini belirle
        canvas.width = maxWidth;
        canvas.height = maxHeight;
    }
}

document.addEventListener("DOMContentLoaded", setCanvasSize);
window.addEventListener("resize", setCanvasSize);


function changeIcon(button) {
    var icon = button.querySelector('.bi');
    if (icon) {
      icon.classList.remove('bi-heartbreak-fill');
      icon.classList.add('bi-heart-fill');
    }
  }
  
  function restoreIcon(button) {
    var icon = button.querySelector('.bi');
    if (icon) {
      icon.classList.remove('bi-heart-fill');
      icon.classList.add('bi-heartbreak-fill');
    }
  }


  