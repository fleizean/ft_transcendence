export function createTournament() {
    var form = document.getElementById('TournamentForm');
    var formData = new FormData(form);
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    fetch('/tournament-create', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: formData
      })
      .then(response => response.text())
      .then(data => {
        if (data.includes("/tournament-room/"))
          swapApp(data);
        else {
          showToast(`${data}`, `text-bg-danger`, `bi bi-bug-fill`);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }