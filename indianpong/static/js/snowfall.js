document.addEventListener('DOMContentLoaded', function () {
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
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarNav = document.querySelector("#navbarNav");

    navbarToggler.addEventListener('click', function (event) {
        event.preventDefault();
        navbarNav.classList.toggle('show');
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const burgerMenu = document.querySelector(".burger-menu");
    const navLinks = document.querySelector(".nav-links");

    burgerMenu.addEventListener('click', function (event) {
        event.preventDefault();
        navLinks.classList.toggle('show');
    });
});
