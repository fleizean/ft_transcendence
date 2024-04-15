function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

export function initializeSearch() {
    
    const followButtons = document.querySelectorAll(".button-follow");
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    followButtons.forEach((button) => {
      button.addEventListener('click', (e) => {
        const username = e.target.getAttribute('data-username');
        const lang = getCookie('selectedLanguage');
        let action = e.target.innerHTML.trim();
        if (action == "अनुसरण करना" || action == "Seguir" || action == "Takip Et" || action == "Follow") {
          action = "follow"
        } else if (action == "अनफ़ॉलो" || action == "Deixar" || action == "Takipten Çık" || action == "Unfollow") {
          action = "unfollow"
        }
        fetch(`/follow_unfollow/${username}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({ action: action })
        })
        .then(response => response.json())
        .then(data => {
          if (data['status'] === 'ok') {
            if (lang == 'hi') {
              e.target.innerHTML = data['action'] === 'follow' ? 'अनफ़ॉलो' : 'अनुसरण करना';
              e.target.style.backgroundColor = data['action'] === 'follow' ? 'black' : '#dc3545';
            }
            else if(lang == 'tr') {
              e.target.innerHTML = data['action'] === 'follow' ? 'Takipten Çık' : 'Takip Et';
              e.target.style.backgroundColor = data['action'] === 'follow' ? 'black' : '#dc3545';
            }
            else if (lang == 'pt') {
              e.target.innerHTML = data['action'] === 'follow' ? 'Deixar' : 'Seguir';
              e.target.style.backgroundColor = data['action'] === 'follow' ? 'black' : '#dc3545';
            }
            else {
              e.target.innerHTML = data['action'] === 'follow' ? 'Unfollow' : 'Follow';
              e.target.style.backgroundColor = data['action'] === 'follow' ? 'black' : '#dc3545';
            }
          }
        });
      }); 
    });
}

export function makeSearch(action) {
  if (!action)
    return;

  var form = document.getElementById('searchForm');
  var formData = new FormData(form);
  var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
  fetch('/search', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: formData
  })
  .then(response => response.text())
  .then(data => {
    document.body.innerHTML = data;
    initializeSearch();
  })
  .catch(error => {
    console.error(error);
  });
}