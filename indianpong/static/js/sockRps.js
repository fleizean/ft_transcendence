// rps.js

export function RemoteRps() {

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

const wsEndpoint = 'wss://' + window.location.host + '/ws/rps/';
const websocket = new WebSocket(wsEndpoint);

const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
const selectedLanguage = cookie ? cookie.split('=')[1] : 'en'; 

const checkbox = document.getElementById('flexSwitchCheckDefault');
const selectedGameModeLabel = document.getElementById('selectedGameMode');
const gameArea = document.getElementById('container-top');
const cheaterButton = document.getElementById('cheater-choice');
const godthingsButton = document.getElementById('godthings-choice');
var gameMode = document.getElementById('selectedGameMode');
const matchmakingButton = document.getElementById('matchmakingButtons');

const ICON_PATH = document.querySelector('.container-top').dataset.iconpath;

const choiceButtons = document.querySelectorAll(".choice-btn");
const gameDiv = document.querySelector(".game");
const resultsDiv = document.querySelector(".results");
const resultDivs = document.querySelectorAll(".results__result");

const resultWinner = document.querySelector(".results__winner");
const resultText = document.querySelector(".results__text");

const scoreNumber1 = document.querySelector(".score__number1");
const scoreNumber2 = document.querySelector(".score__number2");

const player1Picked = document.getElementById("player1_picked");
const player2Picked = document.getElementById("player2_picked");

let cheaterAbilities = false;
let godthingsAbilities = false;

let score = 0;

let abilityStatus = false;

// Prevent animation on load
setTimeout(() => {
    document.body.classList.remove("preload");
}, 500);

// maybe merge with my object
var player1 = {username: '', score: 0};
var player2 = {username: '', score: 0};

var my = {
    username: '', opponent_username: '', game_id: '',
};

function scoreUpdate(player1_score, player2_score) {
    player1.score = player1_score;
    scoreNumber1.innerText = player1_score;
    player2.score = player2_score;
    scoreNumber2.innerText = player2_score;
}

websocket.onopen = function (e) {
    // Show some greeting message
    console.log('WebSocket connection established');
}

websocket.onclose = function (e) {
    // stop the game
    console.error('WebSocket connection closed');
}

websocket.onerror = function (e) {
    console.error('Error: ' + e.data.error);
    // stop the game
}

websocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch (data.type) {
        case 'insearch':
            // Self send message
            console.log('In search', data.user);
            if (my.username === '') {
                my.username = data.user;
            }
            // Take online users usernames and display them
            addUserCount(data.user_count);
            console.log('Online users', data.user_count);
            break;
        
        case 'user.insearch':
            // Send others i joined the lobby
            console.log('User in search', data.user);
            // Add user to online users list
            if (data.user !== my.username) {
                addUserCount(1);
            }

            if (selectedLanguage === 'tr')
                showToast(data.user + ' katıldı!', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'hi')  
                showToast(data.user + ' शामिल हो गया!', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'pt')  
                showToast(data.user + ' entrou!', 'text-bg-success', 'bi bi-check-circle-fill')
            else
                showToast(data.user + ' joined!', 'text-bg-success', 'bi bi-check-circle-fill')
            break;
        case 'user.outsearch':
            // Send others user left the lobby
            console.log('User out search', data.user);
            // Remove user from online users list
            addUserCount(-1);
            if (selectedLanguage === 'tr')
                showToast(data.user + ' ayrıldı!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'hi')
                showToast(data.user + ' चला गया!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'pt')
                showToast(data.user + ' saiu!', 'text-bg-danger', 'bi bi-check-circle-fill')
            else
                showToast(data.user + ' left!', 'text-bg-danger', 'bi bi-check-circle-fill')
            break;
        case 'game.disconnected':
            // stop the game
            gameOverScreen.style.display = 'block'; //? check
            if (selectedLanguage === 'tr')
                showToast(`${data.disconnected} bağlantısı kesildi. Otomatik olarak kazanan sizsiniz`, 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'hi')
                showToast(`${data.disconnected} डिस्कनेक्ट हो गया आप ऑटोमेटिक विनर हैं`, 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'pt')
                showToast(`${data.disconnected} desconectado Você é o vencedor automaticamente`, 'text-bg-danger', 'bi bi-check-circle-fill')
            else    
                showToast(`${data.disconnected} disconnected You are automatically winner`, 'text-bg-danger', 'bi bi-check-circle-fill')
            break;
        case 'start':
            // Start the game
            my.game_id = data.game_id;
            player1.username = data.player1;
            player2.username = data.player2;

            
            gameArea.style.visibility = "visible";
            matchmakingButton.style.display = "none";
            if (abilityStatus) {
                cheaterButton.style.display = 'block';
                godthingsButton.style.display = 'block';
            }

            document.getElementById("player1Name").innerText = player1.username;
            document.getElementById("player2Name").innerText = player2.username;
            
            if (selectedLanguage === 'tr')
                showToast('Oyun başladı', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'hi')
                showToast('खेल शुरू हुआ', 'text-bg-success', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'pt')
                showToast('Jogo começou', 'text-bg-success', 'bi bi-check-circle-fill')
            else
                showToast('Game started', 'text-bg-success', 'bi bi-check-circle-fill')
            break;
        
        case 'matchmaking.notfound':
            // Matchmaking found
            if (selectedLanguage === 'tr')
                showToast('Rakip bulunamadı', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'hi')
                showToast('विरोधी नहीं मिला', 'text-bg-danger', 'bi bi-check-circle-fill')
            else if (selectedLanguage === 'pt')
                showToast('Oponente não encontrado', 'text-bg-danger', 'bi bi-check-circle-fill')
            else
                showToast('No opponent found', 'text-bg-danger', 'bi bi-check-circle-fill')
            break;
        
        case 'result': 
            // Game result
            var result = data.result;
            var game_id = data.game_id;
            var player1_choice = data.player1_choice;
            var player2_choice = data.player2_choice;
            var player1_score = data.player1_score;
            var player2_score = data.player2_score;
            
            if (my.username === player1.username && player1_choice === "LIKEACHEATER")
                cheaterAbilities = true;
            else if (my.username === player2.username && player2_choice === "LIKEACHEATER")
                cheaterAbilities = true;
            if (my.username === player1.username && player1_choice === "GODOFTHINGS")
                godthingsAbilities = true;
            else if (my.username === player2.username && player2_choice === "GODOFTHINGS")
                godthingsAbilities = true;
            
            scoreUpdate(player1_score, player2_score);

            displayResults([player1_choice, player2_choice]);
            displayWinner(result);
            break;

        }
    }

function addUserCount(count) {
    console.log('User count', count);
    var userCountElement = document.getElementById('userCount');
    var currentCount = parseInt(userCountElement.innerText);
    
    userCountElement.innerText = currentCount + count;

}
function searchOpponent() {
    // Search for opponent
    checkbox.disabled = true;
    websocket.send(JSON.stringify({
        type: 'matchmaking'
    }));
}

function sendChoice(choice) {
    // Send choice to opponent
    console.log(choice);
    websocket.send(JSON.stringify({
        type: 'choice',
        game_id: my.game_id,
        choice: choice, // rock, paper, scissors, godthings, cheater
    }));
}

//-------------------


// Game Logic
choiceButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const choiceName = button.dataset.choice;
        sendChoice(choiceName);
        choiceButtons.forEach(btn => {
            btn.disabled = true;
        });
    });
});


function displayResults(results) {
    player1Picked.innerHTML = 
    selectedLanguage === 'tr' ? player1.username + " seçti" :
    selectedLanguage === 'hi' ? player1.username + " चुना" :
    selectedLanguage === 'pt' ? player1.username + " escolheu" :
    player1.username + " picked";

    player2Picked.innerHTML = 
        selectedLanguage === 'tr' ? player2.username + " seçti" :
        selectedLanguage === 'hi' ? player2.username + " चुना" :
        selectedLanguage === 'pt' ? player2.username + " escolheu" :
        player2.username + " picked";

    resultDivs.forEach((resultDiv, idx) => {
        setTimeout(() => {
            
            resultDiv.innerHTML = `
        <div class="choice ${results[idx].toLowerCase()}">
            <img src="${ICON_PATH}icon-${results[idx].toLowerCase()}.svg" alt="${results[idx].toLowerCase()}" />
        </div>
      `;
        }, idx * 1000);
    });

    gameDiv.classList.toggle("hidden");
    resultsDiv.classList.toggle("hidden");
}

function displayWinner(result) {
    setTimeout(() => {
        if (result === "PLAYER1_WIN") {
            var langResult = selectedLanguage === 'tr' ? " kazandı" : selectedLanguage === 'hi' ? " जीता" : selectedLanguage === 'pt' ? " ganhou" : " win";
            resultText.innerText = player1.username + langResult;
            resultDivs[0].classList.toggle("winner");
        } else if (result === "PLAYER2_WIN") {
            var langResult = selectedLanguage === 'tr' ? " kazandı" : selectedLanguage === 'hi' ? " जीता" : selectedLanguage === 'pt' ? " ganhou" : " win";
            resultText.innerText = player2.username + langResult;
            resultDivs[1].classList.toggle("winner");
        } else if (result === "DRAW") {
            var langResult = selectedLanguage === 'tr' ? " berabere" : selectedLanguage === 'hi' ? " बराबरी" : selectedLanguage === 'pt' ? " empate" : " draw";
            resultText.innerText = langResult;
        }
        else {
            var resultWinnerText = selectedLanguage === 'tr' ? " oyunu kazandı" : selectedLanguage === 'hi' ? " जीत गया" : selectedLanguage === 'pt' ? " ganhou o jogo" : " won the game";
            if (player1.score > player2.score)
                resultWinner.innerText = player1.username + resultWinnerText;
            else
                resultWinner.innerText = player2.username + resultWinnerText;
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("hidden");
            showGameOverScreen();
        }
        resultWinner.classList.toggle("hidden");
    }, 1000);
    if (result != "OVER") {
        setTimeout(() => {
            if (cheaterAbilities)
                cheaterButton.style.display = "none";
            else if (godthingsAbilities)
                godthingsButton.style.display = "none";
            gameDiv.classList.toggle("hidden");
            resultsDiv.classList.toggle("hidden");

            resultDivs.forEach((resultDiv) => {
                resultDiv.innerHTML = "";
                resultDiv.classList.remove("winner");
            });
        
            resultText.innerText = "";
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("show-winner");

            choiceButtons.forEach(btn => {
                btn.disabled = false;
            });
        }, 3000);
    }
}

function showGameOverScreen() {
    var winnerText = (player1.score == 3) ? player1.username : player2.username;
    document.getElementById('winnerText').innerText =  selectedLanguage === 'tr' ? winnerText + " kazandı" : selectedLanguage === 'hi' ? winnerText + " जीता" : selectedLanguage === 'pt' ? winnerText + " ganhou" : winnerText + " win";
    document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(11, 22, 8, 0.8)';
    document.getElementById('gameOverScreen').style.display = 'block';
}

document.getElementById('ponggamebtn').addEventListener('click', searchOpponent);

checkbox.addEventListener('change', function() {
    // Checkbox'un durumuna göre etiketin innerHTML değerini değiştirme
    if (checkbox.checked) {
        gameMode = "Abilities";
        abilityStatus = true;
        if (selectedLanguage === 'tr')
            selectedGameModeLabel.innerHTML = "Yetenekler";
        else if (selectedLanguage === 'hi')
            selectedGameModeLabel.innerHTML = "क्षमताएँ";
        else if (selectedLanguage === 'pt')
            selectedGameModeLabel.innerHTML = "Habilidades";
        else
            selectedGameModeLabel.innerHTML = "Abilities";
    } else {
        gameMode = "Vanilla";
        abilityStatus = false;
        if (selectedLanguage === 'tr')
            selectedGameModeLabel.innerHTML = "Vanilya";
        else if (selectedLanguage === 'hi')
            selectedGameModeLabel.innerHTML = "वैनिला";
        else if (selectedLanguage === 'pt')
            selectedGameModeLabel.innerHTML = "Baunilha";
        else
            selectedGameModeLabel.innerHTML = "Vanilla";
    }
});

const gameModeSelect = document.getElementById("gameModeSelect");

gameModeSelect.addEventListener("mouseenter", function() {
    document.querySelector(".game-mode-info").style.display = "block";
});

gameModeSelect.addEventListener("mouseleave", function() {
    document.querySelector(".game-mode-info").style.display = "none";
});
// Show/Hide Rules

document.getElementById('exitButton').addEventListener('click', exitGame);

function exitGame() {
    swapApp('/rps-game-find')
}
}