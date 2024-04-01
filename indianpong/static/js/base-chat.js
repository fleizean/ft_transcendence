export function getChat(username) {
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    fetch(`/start_chat/${username}`, {  // URL'yi dinamik olarak oluştur
        method: 'POST',
        body: JSON.stringify({ username: username }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => response.json())
    .then(data => {
        const roomId = data.room_id;
        
        // Chat odası için yeni bir URL oluştur
        const newUrl = `/chat/${roomId}/`;  // URL'yi bu şekilde güncelle
        swapApp(newUrl);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
