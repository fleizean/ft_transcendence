    export function getChat(username) {
    if (!username) {
        return;
    }

    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    
    fetch(`/start_chat/${username}`, {
        method: 'POST',
        body: JSON.stringify({ username: username }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (!data.room_id) {
            throw new Error('Invalid response: missing room_id');
        }
        
        const roomId = data.room_id;
        const newUrl = `/chat/${roomId}/`;
        swapApp(newUrl);
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
}
