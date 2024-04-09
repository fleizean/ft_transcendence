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
    })
    .catch(error => {
        console.error('Error starting tournament:', error);
    });
}