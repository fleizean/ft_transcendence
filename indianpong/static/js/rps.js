
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

const MAX_SCORE_RPS = 3;
let score = 0;

// Game Logic
choiceButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const choiceName = button.dataset.choice;
        const choice = CHOICES.find((choice) => choice.name === choiceName);
        choose(choice);
    });
});

function choose(choice) {
    const aichoice = aiChoose();
    displayResults([choice, aichoice]);
    displayWinner([choice, aichoice]);
}

function aiChoose() {
    const rand = Math.floor(Math.random() * CHOICES.length);
    return CHOICES[rand];
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
    document.getElementById('winnerText').innerText = winnerText;
    var winnerText = (scoreNumber1 == MAX_SCORE_RPS) ? "YOU WIN!" : "";
    console.log("TEST")
    if (scoreNumber1 > scoreNumber2) {
        document.getElementById('gameOverScreen').style.backgroundColor = 'rgba(11, 22, 8, 0.8)';
    }
    else {
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
    PlayAgainRPS();
}

function exitGame() {
    window.location.href = '/rps-game-find';
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

function  PlayAgainRPS() {

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
