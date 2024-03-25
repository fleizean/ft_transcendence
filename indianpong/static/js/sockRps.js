// rps.js

const wsEndpoint = 'ws://' + window.location.host + '/ws/rps/';
const websocket = new WebSocket(wsEndpoint);

const translationswin = {
    'hi': 'आप जीत गए',
    'pt': 'você ganhou',
    'tr': 'kazandınız',
    'en': 'you win' // Varsayılan İngilizce metin
};

const translationslose = {
    'hi': 'आप हार गए',
    'pt': 'você perdeu',
    'tr': 'kaybettiniz',
    'en': 'you lose' // Varsayılan İngilizce metin
};

const CHOICES = [
    {
        name: "paper",
        beats: "rock",
    },
    {
        name: "scissors",
        beats: "paper",
    },
    {
        name: "rock",
        beats: "scissors",
    },
    {
        name: "godthings",
        beats: "all",
    },
    {
        name: "cheater",
        beats: "all",
    }
];

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
    player2.score = player2_score;
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
    console.error('Error: ' + e.data);
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
            showToast(`${data.disconnected} disconnected You are automatically winner`, 'text-bg-danger', 'bi bi-check-circle-fill')
            console.log('Player disconnected', data.disconnected);
            break;
        case 'start':
            // Start the game
            my.game_id = data.game_id;
            player1 = data.player1;
            player2 = data.player2;
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
            showToast('No opponent found', 'text-bg-danger', 'bi bi-check-circle-fill')
            break;
        
        case 'result': 
            // Game result
            result = data.result;
            game_id= data.game_id,
            player1_score = data.player1_score,
            player2_score = data.player2_score,
            scoreUpdate(player1_score, player2_score);

            switch (result) {
                case 'PLAYER1_WIN':
                    break;
                case 'PLAYER2_WIN':
                    break;
                case 'DRAW':
                    break;
                case 'OVER':
                    break;
            }

            break;    

        }
    }

function addUserCount(count) {
    var userCountElement = document.getElementById('userCount');
    var currentCount = parseInt(userCountElement.innerText);
    
    if (!isNaN(count) || count !== undefined) {
        userCountElement.innerText = currentCount + count;
    }
}

function searchOpponent() {
    // Search for opponent
    websocket.send(JSON.stringify({
        type: 'matchmaking',
    }));
}

function sendChoicce(choice) {
    // Send choice to opponent
    websocket.send(JSON.stringify({
        type: 'choice',
        game_id: my.game_id,
        choice: choice, // rock, paper, scissors
    }));
}

function sendAbility(ability) {
    // Send ability to opponent
    websocket.send(JSON.stringify({
        type: 'ability',
        game_id: my.game_id,
        ability: ability, // shield, heal, attack
    }));
}

//-------------------

const ICON_PATH = document.querySelector('.container-top').dataset.iconpath;

const choiceButtons = document.querySelectorAll(".choice-btn");
const gameDiv = document.querySelector(".game");
const resultsDiv = document.querySelector(".results");
const resultDivs = document.querySelectorAll(".results__result");

const resultWinner = document.querySelector(".results__winner");
const resultText = document.querySelector(".results__text");

const playAgainBtn = document.querySelector(".play-again");

const scoreNumber1 = document.querySelector(".score__number1");
const scoreNumber2 = document.querySelector(".score__number2");
let score = 0;

// Game Logic
choiceButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const choiceName = button.dataset.choice;
        const choice = CHOICES.find((choice) => choice.name === choiceName);
        sendChoice(choiceName);
        choose(choice);

        // Seçimi WebSocket üzerinden gönder
        const dataToSend = { choice: choiceName };
        websocket.send(JSON.stringify(dataToSend));
    });
});



function choose(choice) {
    const aichoice= opponentChoice;
    displayResults([choice, aichoice]);
    displayWinner([choice, aichoice]);

}


function displayResults(results) {

    resultDivs.forEach((resultDiv, idx) => {
        setTimeout(() => {
            resultDiv.innerHTML = `
        <div class="choice ${results[idx].name}">
            <img src="${ICON_PATH}icon-${results[idx].name}.svg" alt="${results[idx].name}" />
        </div>
      `;
        }, idx * 1000);
    });

    gameDiv.classList.toggle("hidden");
    resultsDiv.classList.toggle("hidden");
}

function displayWinner(results) {
    setTimeout(() => {
        const userWins = isWinner(results);
        const aiWins = isWinner(results.reverse());

        if (userWins) {
            resultText.innerText = "you win";
            resultDivs[0].classList.toggle("winner");
            keepScore(1);
        } else if (aiWins) {
            resultText.innerText = "you lose";
            resultDivs[1].classList.toggle("winner");
            keepScore(-1);
        } else {
            resultText.innerText = "draw";
        }
        if (3 == parseInt(scoreNumber1.innerText)) {
            resultWinner.innerText = "You win the game";
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("show-winner");
            showGameOverScreen();
        }
        else if (3 == parseInt(scoreNumber2.innerText)) {
            resultWinner.innerText = "You lose the game";
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("show-winner");
            showGameOverScreen();
        }
        else {
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("show-winner");
            showGameOverScreen();
        }

    }, 1000);
}

function showGameOverScreen() {

    document.getElementById('winnerText').innerText = winnerText;
    document.getElementById('loserText').innerText = loserText;
    var winnerText = (scoreNumber1 == MAX_SCORE) ? "YOU WIN!" : "";
    var loserText = (scoreNumber2 == MAX_SCORE) ? "YOU LOSE!" : "";
    if (scoreNumber1 > scoreNumber2) {
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(11, 22, 8, 0.8)';
    }
    else {
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(20, 5, 5, 0.8)';
    }
    document.getElementById('gameOverScreen').style.display = 'block';
}


function isWinner(results) {
    return results[0].beats === results[1].name;
}

function keepScore(point) {
    const tempscore = Math.abs(point);
    if (point > 0) {
        scoreNumber1.innerText = parseInt(scoreNumber1.innerText) + tempscore;
    } else {
        scoreNumber2.innerText = parseInt(scoreNumber2.innerText) + tempscore;
    }
}

// Play Again
playAgainBtn.addEventListener("click", () => {
    gameDiv.classList.toggle("hidden");
    resultsDiv.classList.toggle("hidden");

    resultDivs.forEach((resultDiv) => {
        resultDiv.innerHTML = "";
        resultDiv.classList.remove("winner");
    });

    resultText.innerText = "";
    resultWinner.classList.toggle("hidden");
    resultsDiv.classList.toggle("show-winner");
});

// Show/Hide Rules
