var isRPSVisibleHistory = true; 

export function matchHistoryChanger(status) {
    
    if (!status)
        return;
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

export function toggleGame(status) {
    if (!status)
        return;
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

export function followButton(username) {
    if(!username)
        return;
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    var button = document.getElementById('followbtn');
    var button2 = document.getElementById('unfollowbtn');
    fetch(`/follow_unfollow/${username}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ action: "follow" })
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 'ok') {
            button.style.display = 'none';
            button2.style.display = 'block';    
        }
    });
}

export function unfollowButton(username) {
    if(!username)
        return;
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    var button = document.getElementById('unfollowbtn');
    var button2 = document.getElementById('followbtn');
    fetch(`/follow_unfollow/${username}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ action: "unfollow" })
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 'ok') {
            button.style.display = 'none';
            button2.style.display = 'block';
        }
    });
}
