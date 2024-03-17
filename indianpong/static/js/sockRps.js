// rps.js

const wsEndpoint = 'ws://' + window.location.host + '/ws/rps/';
const websocket = new WebSocket(wsEndpoint);

websocket.onopen = () => {
    console.log('WebSocket connected');
};

// Prevent animation on load
setTimeout(() => {
    document.body.classList.remove("preload");
}, 500);


let canChoose = false;
var game_id = null;
var opponentChoice = null;

websocket.onmessage = function (e) {
    var data = JSON.parse(e.data)
    if (data.message) {
        alert(data.message)
        if (data.message.startsWith('You have been matched')) {
            // The user has been matched with another player
            // Hide the 'Join Queue' button and show the game container
            document.getElementById('ponggamebtn').style.visibility = 'hidden';
            document.getElementById('container-top').style.visibility = 'visible';
        }
    }
    if (data.type === 'game_id') {
        console.log(data.game_id)
        game_id = data.game_id;
        document.getElementById('ponggamebtn').style.visibility = 'hidden';
        document.getElementById('container-top').style.visibility = 'visible';
    }
    if (data.queue_count) {
        document.getElementById('queueCount').innerText = data.queue_count
    }
    if (data.action === 'choose_hand') {
        canChoose = true;
        const dataChoice = data.opponent_choices;
        const choiceName = dataChoice;
        const choice = CHOICES.find((choice) => choice.name === choiceName);
        opponentChoice = choice;
        console.log('opponent choice', choice);
    }
}

function sendChoice(choice) {
    websocket.send(
        JSON.stringify({
            action: 'choose_hand',
            choices: choice,
            scoreNumber1: scoreNumber1,
            scoreNumber2: scoreNumber2,
        })
    )
}

function endGame() {
    websocket.send(
        JSON.stringify({
            action: 'end_game',
            winner: scoreNumber1.innerText > scoreNumber2.innerText ? 'player1' : 'player2',
            loser: scoreNumber1.innerText < scoreNumber2.innerText ? 'player1' : 'player2',
            scoreNumber1: scoreNumber1.innerText,
            scoreNumber2: scoreNumber2.innerText,
            gameId: game_id,
        })
    )
}

function joinQueue() {
    // "rps-buttons" yerine "container-top" kullanıyoruz
    websocket.send(
        JSON.stringify({
            action: 'join_queue'
        })
    )
}

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
];

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
        setTimeout(() => {
            choose(choice);
        }, 5000);
        canChoose = false;

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
    console.log("TEST")
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
