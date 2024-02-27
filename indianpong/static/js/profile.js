
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
