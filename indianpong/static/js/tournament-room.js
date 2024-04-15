export function showToast(content, status, iconClass) {
    if (!content || !status || !iconClass)
        return;

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
    setTimeout(function() {
        toast.hide();
    }, 8000);
  }

export function displaySectionGame(sectionId) {
    if (!sectionId)
        return;
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

export function joinTournament(tournamentId) {
    if (!tournamentId)
        return;
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    const formData = new FormData();
    


    formData.append('join_tournament', 'true');

    fetch(`/tournament-room/${tournamentId}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }, 
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        const error = document.querySelector('.container-top').dataset.error;
        const sucess = document.querySelector('.container-top').dataset.sucess;
        if (error)
            showToast(error, 'text-bg-danger', 'bi bi-x');
        else if (sucess)
            showToast(sucess, 'text-bg-success', 'bi bi-check');
    })
    .catch(error => {
        console.error('Error joining tournament:', error);
    });
}

export function startTournament(tournamentId) {
    if (!tournamentId)
        return;
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    const formData = new FormData();
    
    formData.append('start_tournament', 'true');

    fetch(`/tournament-room/${tournamentId}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }, 
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        const error = document.querySelector('.container-top').dataset.error;
        const sucess = document.querySelector('.container-top').dataset.sucess;
        if (error)
            showToast(error, 'text-bg-danger', 'bi bi-x');
        else if (sucess)
            showToast(sucess, 'text-bg-success', 'bi bi-check');
    })
    .catch(error => {
        console.error('Error starting tournament:', error);
    });
}

export function leaveTournament(tournamentId) {
    if (!tournamentId)
        return;
    const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
    const lang = cookie ? cookie.split('=')[1] : 'en';
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    const formData = new FormData();
    formData.append('leave_tournament', 'true');

    fetch(`/tournament-room/${tournamentId}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }, 
    })
    .then(response => response.text())
    .then(data => {
        if (lang === 'tr')
            showToast('Turnuvadan ayrıldınız.', 'text-bg-danger', 'bi bi-check');
        else if (lang === 'hi')
            showToast('आपने टूर्नामेंट छोड़ दिया है।', 'text-bg-danger', 'bi bi-check');
        else if (lang === 'pt')
            showToast('Você saiu do torneio.', 'text-bg-danger', 'bi bi-check');
        else
            showToast('You have left the tournament.', 'text-bg-danger', 'bi bi-check');

        setTimeout(function() {
            swapApp('/tournament-room-list');
        }, 1000);
    })
    .catch(error => {
        console.error('Error leaving tournament:', error);
    });
}