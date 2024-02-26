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

var sections = ["profile_form", "social_form", "delete_account_form", "blockedUsers", "password_form"];


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

    
    function showPassword(input) {
        var passwordField = document.getElementById(input);
        passwordField.type = "text";
    }

    function hidePassword(input) {
        var passwordField = document.getElementById(input);
        passwordField.type = "password";
    }

function activateCreateRoom() {
    var value = document.getElementById("createRoom-popup");
    var overlay = document.getElementById("overlay");
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


var isRPSVisibleHistory = true; 

function matchHistoryChanger() {
    var switcherBtn = document.querySelector(".changer-btn");
    var historyPong = document.getElementById('match-history-pong');
    var historyRPS = document.getElementById('match-history-rps');
    
    if (isRPSVisibleHistory) {
        // Ping pong istatistiklerini göster
        historyPong.style.display = 'block';
        historyRPS.style.display = 'none';
        switcherBtn.innerHTML = '🏓'; // HTML içeriğine Unicode karakterini ekleyin
    } else {
        // RPS istatistiklerini göster
        historyPong.style.display = 'none';
        historyRPS.style.display = 'block';
        switcherBtn.innerHTML = '✂️'; // HTML içeriğine Unicode karakterini ekleyin
    }
    
    // Durumu tersine çevir
    isRPSVisibleHistory = !isRPSVisibleHistory;
}

var isRPSVisibleStats = true; 

function toggleGame() {
    var switcherBtn = document.querySelector(".switch-btn");
    var statsPong = document.getElementById('stats-info-pong');
    var statsRPS = document.getElementById('stats-info-rps');

    if (isRPSVisibleStats) {
        // Ping pong istatistiklerini göster
        statsPong.style.display = 'block';
        statsRPS.style.display = 'none';
        switcherBtn.innerHTML = '🏓'; // HTML içeriğine Unicode karakterini ekleyin
    } else {
        // RPS istatistiklerini göster
        statsPong.style.display = 'none';
        statsRPS.style.display = 'block';
        switcherBtn.innerHTML = '✂️'; // HTML içeriğine Unicode karakterini ekleyin
    }
    
    // Durumu tersine çevir
    isRPSVisibleStats = !isRPSVisibleStats;
}
