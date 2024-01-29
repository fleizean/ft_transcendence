/* document.addEventListener('DOMContentLoaded', function () {
    // Hemen çalıştırılacak kod buraya eklenecek

    const cover = document.querySelector('.snow-class');

    for (let i = 1; i < 100; i++) {
        const snowFlake = document.createElement('div');
        snowFlake.className = 'snow';
        cover.appendChild(snowFlake);

        const size = Math.random() * 3;
        snowFlake.style.width = `${size}px`;
        snowFlake.style.height = `${size}px`;

        const delay = Math.random();
        snowFlake.style.animation = `snowRain 5s linear ${delay}s infinite`;

        const left = Math.random() * 100;
        snowFlake.style.left = `${left}vw`;

        const animationDuration = 5 + Math.random() * 5;
        snowFlake.style.animationDuration = `${animationDuration}s`;

        // Kar tanelerini ilk 3 saniye boyunca görünmez yap
        snowFlake.style.opacity = 0;
        snowFlake.style.animationPlayState = 'running';

        // Zamanlayıcı ile 3 saniye sonra görünürlüğü aç
        setTimeout(() => {
            snowFlake.style.opacity = 1;
            snowFlake.style.animationPlayState = 'running';
        }, 1300);

    
    }
});
 */



/* 2FA Alanı Başlangıç */
function clear2FA() {
    const inputFields = document.querySelectorAll('.input-fields input');
    inputFields.forEach(input => {
        input.value = '';
    });
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

/* 2FA Alanı Bitiş */




function getFutureDate() {
    // Şu anki tarihi al
    var currentDate = new Date();

    // 10 gün ekleyerek gelecek tarihi al
    var futureDate = new Date();
    futureDate.setDate(currentDate.getDate() + 10);

    // Tarih formatını ayarla (gün/ay/yıl)
    var day = futureDate.getDate();
    var month = futureDate.getMonth() + 1; // Ay 0'dan başlar, bu yüzden 1 ekleyin
    var year = futureDate.getFullYear();

    // Formatı oluştur
    var formattedDate = day + '/' + month + '/' + year;

    return formattedDate;
}

function activateCreateRoom() {
    var value = document.getElementById("createRoom-popup");
    var overlay = document.getElementById("overlay");
    if (value) {
        value.style.display = 'flex';
        overlay.style.display = 'block';

    }
}

/* Şu anlık çalışmıyor çünkü click izlemeleri divin router özelliği yüzünden sıkıntılı
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
  }); */

 
function closeCreateRoom() {
    var value = document.getElementById("createRoom-popup");
    var overlay = document.getElementById("overlay");
    if (value) {
        value.style.display = 'none';
        overlay.style.display = 'none';
    }
}


function displaySection(sectionId) {
    var sections = ["editProfile", "addSocial", "closeAccount", "changePassword", "google2FA", "blockedUsers"];

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

jQuery(document).ready(function ($) {
    $(".navbar-toggler").on("click", function () {
      $("#navbarNav").toggleClass("show");
    });
  });

jQuery(document).ready(function () {
    $(".burger-menu").click(function () {
        $(".nav-links").toggleClass('show');
    });
});

$(document).ready(function () {
    // Handle the click event on the navbar toggler button
    $('#profileNavbar .navbar-toggler').click(function () {
        // Toggle the 'show' class on the navbar collapse
        $('#profileNavLinks').toggleClass('show');
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