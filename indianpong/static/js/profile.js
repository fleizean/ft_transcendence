
var isRPSVisibleHistory = true; 

function matchHistoryChanger() {
    var switcherBtn = document.querySelector(".changer-btn");
    var historyPong = document.getElementById('match-history-pong');
    var historyRPS = document.getElementById('match-history-rps');
    isRPSVisibleHistory = !isRPSVisibleHistory;

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
}

var isRPSVisibleStats = true; 

function toggleGame() {
    var switcherBtn = document.querySelector(".switch-btn");
    var statsPong = document.getElementById('stats-info-pong');
    var statsRPS = document.getElementById('stats-info-rps');
    isRPSVisibleStats = !isRPSVisibleStats;

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
}

const followButtons = document.querySelectorAll(".btn, .unfollow-btn");
followButtons.forEach((button) => {
    button.addEventListener('click', (e) => {
        const username = e.target.getAttribute('data-username');
        const action = e.target.classList.contains('unfollow-btn') ? 'unfollow' : 'follow';
        fetch(`/follow_unfollow/${username}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok') {
                if (action === 'follow') {
                  e.target.innerHTML = '<i class="bi bi-heartbreak-fill"></i> Unfollow';
                  e.target.classList.add('unfollow-btn');
                  e.target.classList.remove('btn', 'btn-danger');
                } else {
                  e.target.innerHTML = '<i class="bi bi-heart-fill"></i> Follow';
                  e.target.classList.remove('unfollow-btn');
                  e.target.classList.add('btn', 'btn-danger');
                }
              }
        });
    });
});