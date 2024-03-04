
// Prevent animation on load
setTimeout(() => {
    document.body.classList.remove("preload");
}, 200);


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
const choiceButtons = document.querySelectorAll(".choice-btn");
const gameDiv = document.querySelector(".game");
const resultsDiv = document.querySelector(".results");
const resultDivs = document.querySelectorAll(".results__result");

const resultWinner = document.querySelector(".results__winner");
const resultText = document.querySelector(".results__text");

const playAgainBtn = document.querySelector(".play-again");

const scoreNumber1 = document.querySelector(".score__number1");
const scoreNumber2 = document.querySelector(".score__number2");

const cheater = document.querySelector('.container-top').dataset.cheater;
const godthings = document.querySelector('.container-top').dataset.godthings;
const username = document.querySelector('.container-top').dataset.username;

const ischeater = (cheater === "true") ? true : false;
const isgodthings = (godthings === "true") ? true : false;

var start_time;

let cheatercount = 0;
let godthingscount = 0;
let aicheatercount = 0;
let aigodthingscount = 0;
let nowChoice = "";

let aicheater = "inactive";

const MAX_SCORE_RPS = 3;
let score = 0;

// Game Logic
choiceButtons.forEach((button) => {
    button.addEventListener("click", () => {
        if (!start_time)
            start_time = new Date();
        const choiceName = button.dataset.choice;
        const choice = CHOICES.find((choice) => choice.name === choiceName);
        nowChoice = choice.name;
        choose(choice);
    });
});

function choose(choice) {
    // Cheater kontrolü
    const aichoice = aiChoose();
    if (choice.name === "cheater" && ischeater  === true && cheatercount < 1) {
        cheatercount++;
        document.getElementById("cheater-choice").style.display = "none";
    }
    if (choice.name === "godthings" && isgodthings === true && godthingscount < 1) {
        godthingscount++;
        document.getElementById("godthings-choice").style.display = "none";
    }
    // Godthings değilse normal oyun kurallarını uygula
    displayResults([choice, aichoice]);
    displayWinner([choice, aichoice]);

}

function aiChoose() {
    var filteredChoices = [];
    var choice = "";
    if (cheater === "true" && godthings !== "true" && aicheatercount < 1) {
        aicheatercount++;
        filteredChoices = CHOICES.filter(choice => choice.name !== "godthings");
        choice = filteredChoices[Math.floor(Math.random() * filteredChoices.length)];
    } else if (godthings === "true" && cheater !== "true" && aigodthingscount < 1) {
        aigodthingscount++;
        filteredChoices = CHOICES.filter(choice => choice.name !== "cheater");
        choice = filteredChoices[Math.floor(Math.random() * filteredChoices.length)];
    } else if (godthings === "true" && cheater === "true" && (aicheatercount < 1 || aigodthingscount < 1)) {
        if (aicheatercount > 0 )
            filteredChoices = CHOICES.filter(choice => choice.name !== "cheater");
        else if (aigodthingscount > 0)
            filteredChoices = CHOICES.filter(choice => choice.name !== "godthings");
        else
            filteredChoices = CHOICES;
        choice = filteredChoices[Math.floor(Math.random() * CHOICES.length)];
        if (choice.name === "cheater")
            aicheatercount++;
        else if (choice.name === "godthings")
            aigodthingscount++;
    } else {
        filteredChoices = CHOICES.filter(choice => choice.name !== "cheater" && choice.name !== "godthings");
        choice = filteredChoices[Math.floor(Math.random() * filteredChoices.length)];
    }
    return choice;
}


function displayResults(results) {
    resultDivs.forEach((resultDiv, idx) => {
        setTimeout(() => {
            resultDiv.innerHTML = `
        <div class="choice ${results[idx].name}">
            <img src="../../static/assets/rps/icon-${results[idx].name}.svg" alt="${results[idx].name}" />
        </div>
      `;
        }, idx * 1000);
    });

    gameDiv.classList.toggle("hidden");
    resultsDiv.classList.toggle("hidden");
}

function displayWinner(results) {
    setTimeout(() => {
        const winner = isWinner(results);

        if (winner == "user") {
            resultText.innerText = "you win";
            resultDivs[0].classList.toggle("winner");
            keepScore(1, results[0].name);
        } else if (winner == "ai") {
            resultText.innerText = "you lose";
            resultDivs[1].classList.toggle("winner");
            keepScore(-1, results[1].name);

        } else {
            resultText.innerText = "draw";
        }

        if (MAX_SCORE_RPS == parseInt(scoreNumber1.innerText) || MAX_SCORE_RPS == parseInt(scoreNumber2.innerText)) {
            showGameOverScreenRPS();
        }
        else {
            resultWinner.classList.toggle("hidden");
            resultsDiv.classList.toggle("show-winner");
        }

    }, 1000);
}

function showGameOverScreenRPS() {

    resultsDiv.classList.toggle("show-winner");
    var winnerText = (scoreNumber1.innerText == MAX_SCORE_RPS) ? "YOU WIN!" : "YOU LOSE";
    document.getElementById('winnerText').innerText = winnerText;
    if (parseInt(scoreNumber1.innerText) > parseInt(scoreNumber2.innerText)) {
        sendWinnerToBackend(username, "IndianAI", parseInt(scoreNumber1.innerText), parseInt(scoreNumber2.innerText), start_time);
        document.getElementById('winnerText').style.color = 'green';
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(11, 22, 8, 0.8)';
    }
    else {
        sendWinnerToBackend("IndianAI", username, parseInt(scoreNumber2.innerText), parseInt(scoreNumber1.innerText), start_time);
        document.getElementById('winnerText').style.color = 'red';
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(20, 5, 5, 0.8)';
    }
    document.getElementById('gameOverScreen').style.display = 'block';
}

document.getElementById('restartButton').addEventListener('click', resetGameRPS);
document.getElementById('exitButton').addEventListener('click', exitGame);

function resetGameRPS() {
    document.getElementById('gameOverScreen').style.display = 'none';
    scoreNumber1.innerText = 0;
    scoreNumber2.innerText = 0;
    cheatercount = 0;
    godthingscount = 0;
    aicheatercount = 0;
    aigodthingscount = 0;
    PlayAgainRPS();
}

function exitGame() {
    window.location.href = '/rps-game-find';
}


function isWinner(results) {
    const player1 = results[0].name;
    const player2 = results[1].name;

    if (player1 === player2 || (player1 === "godthings" && player2 === "cheater") || (player1 === "cheater" && player2 === "godthings")) {
        return "draw";
    }

    // İlk oyuncunun seçimi Godthings ise ve ikinci oyuncu Godthings değilse, ilk oyuncu kazanır
    if (player1 === "godthings" && player2 !== "godthings") {
        return "user";
    }

    // İkinci oyuncunun seçimi Godthings ise ve ilk oyuncu Godthings değilse, ikinci oyuncu kazanır
    if (player2 === "godthings" && player1 !== "godthings") {
        return "ai";
    }

    // İlk oyuncunun seçimi Cheater ise ve ikinci oyuncu Cheater değilse, ilk oyuncu kazanır
    if (player1 === "cheater" && player2 !== "cheater") {
        return "user";
    }

    // İkinci oyuncunun seçimi Cheater ise ve ilk oyuncu Cheater değilse, ikinci oyuncu kazanır
    if (player2 === "cheater" && player1 !== "cheater") {
        return "ai";
    }

    // İki oyuncudan birinin seçimi Godthings veya Cheater ise ve diğeri değilse, bu oyuncu kazanır
    if (player1 === "godthings" || player1 === "cheater" || player2 === "godthings" || player2 === "cheater") {
        return player1 === "godthings" || player1 === "cheater" ? "user" : "ai";
    }

    // Diğer durumda, kazananı belirlemek için normal kuralları kullan
    return results[0].beats === results[1].name ? "user" : "ai";
}

function keepScore(point, name) {
    const tempscore = Math.abs(point);
    if (point > 0) {
        scoreNumber1.innerText = parseInt(scoreNumber1.innerText) + tempscore;
        if (name === "cheater" && parseInt(scoreNumber2.innerText) > 0)
            scoreNumber2.innerText = parseInt(scoreNumber2.innerText) - 1;
    } else {
        scoreNumber2.innerText = parseInt(scoreNumber2.innerText) + tempscore;
        if (name === "cheater" && parseInt(scoreNumber1.innerText) > 0)
            scoreNumber1.innerText = parseInt(scoreNumber1.innerText) - tempscore;
    }
}

function PlayAgainRPS() {
    gameDiv.classList.toggle("hidden");
    resultsDiv.classList.toggle("hidden");
    
    resultDivs.forEach((resultDiv) => {
        resultDiv.innerHTML = "";
        resultDiv.classList.remove("winner");
    });

    //resultText.innerText = "";
    //resultWinner.classList.toggle("hidden");
    resultsDiv.classList.toggle("show-winner");
    
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

function sendWinnerToBackend(winner, loser, winnerscore, loserscore, start_time) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var finish_time = new Date();
    const data = {
        game: "rps",
        winner: winner,
        loser: loser,
        winnerscore: winnerscore,
        loserscore: loserscore,
        start_time: start_time,
        finish_time: finish_time
    };

    fetch('update_winner', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        
    })
    .catch(error => {
        console.error('There was a problem updating the winner:', error);
    });
}