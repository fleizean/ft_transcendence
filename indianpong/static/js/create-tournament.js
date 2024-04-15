export function createTournament() {


function showToast(content, status, iconClass) {
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