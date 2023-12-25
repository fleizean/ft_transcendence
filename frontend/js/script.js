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

function displaySection(sectionId) {
    var sections = ["editProfile", "addSocial", "closeAccount", "changePassword", "google2FA"];

    for (var i = 0; i < sections.length; i++) {
        var section = document.getElementById(sections[i]);
        if (sections[i] === sectionId) {
            section.style.display = 'block';
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


/* Game Stats Dashboard */

//pie
var ctxP = document.getElementById("pieChart").getContext('2d');
var myPieChart = new Chart(ctxP, {
  type: 'pie',
  data: {
    labels: ["Red", "Green", "Yellow", "Grey", "Dark Grey"],
    datasets: [{
      data: [300, 50, 100, 40, 120],
      backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
      hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
    }]
  },
  options: {
    responsive: true
  }
});