import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Dashboard");
    }

    async getHtml() {
        return `
        <nav class="navbar">
        <div class="logo-container"><a href="/dashboard" data-link>
          <div class="logo">
            <img src="../../assets/logo.png" alt="IndianPong Logo" width="48" height="48">
            IndianPong
          </div></a>
      </div>
        <ul class="nav-links">
          <li><a href="/dashboard" data-link><i class="bi bi-house-door-fill"></i>Dashboard</a></li>
          <li><a href="/game" data-link><i class="bi bi-play-circle-fill"></i>Game</a></li>
          <li><a href="/chat" data-link><i class="bi bi-chat-fill"></i>Chat</a></li>
          <li><a href="/friends" data-link><i class="bi bi-heart-fill"></i>Friends</a></li>
          <li><a href="/search" data-link><i class="bi bi-binoculars-fill"></i>Search</a></li>
          <li><a href="/profile" data-link><i class="bi bi-person-fill"></i>Profile</a></li>
        </ul>
        <div class="burger-menu">&#9776;</div>
      </nav>

      <div class="container-top">
  <div class="card">
    <div class="page-rotation">
      <h1>Welcome to IndianPong %Name</h1>
      <p>Indian Pong is a collaborative project developed for the 42 school community, offering a nostalgic gaming experience through the classic Atari game, Ping-Pong. This platform allows users to engage in Ping-Pong matches with each other, fostering a sense of friendly competition. In addition to the gaming aspect, Indian Pong provides a social dimension, featuring chat rooms where users can communicate and connect with one another. The platform also enables users to expand their network by adding friends within the 42 school community. Overall, Indian Pong combines the joy of retro gaming with modern social interaction, creating a vibrant and interactive experience for the 42 school community.</p>
      <div class="stats">
        <div class="stat-item card">
          <h3>Games Played</h3>
          <div class="stat-icon">
            <img src="../../assets/gamesplayed.webp" alt="Games Played Illustrator">
          </div>
          <p>42</p>
        </div>
        <div class="stat-item card">
          <h3>Wins</h3>
          <div class="stat-icon">
            <img src="../../assets/winner.png" alt="Win Illustrator">
          </div>
          <p>30</p>
        </div>
        <div class="stat-item card">
          <h3>Losses</h3>
          <div class="stat-icon">
            <img src="../../assets/lose.png" alt="Lose Illustrator">
          </div>
          <p>12</p>
        </div>
        <div class="stat-item card">
          <h3>Friends</h3>
          <div class="stat-icon">
            <img src="../../assets/friend.png" alt="Friend Illustrator">
          </div>
          <p>0</p>
        </div>
      </div>
      <div class="stats">
        <div class="stat-item card">
          <h3>Win Rate %</h3>
          <div class="stat-icon">
            <img src="../../assets/winrate.webp" alt="Win Rate Illustrator">
          </div>
          <p>0</p>
        </div>
        <div class="stat-item card">
          <h3>Win Streak</h3>
          <div class="stat-icon">
            <img src="../../assets/winstreak.png" alt="Win Streak Illustrator">
          </div>
          <p>0</p>
        </div>
        <div class="stat-item card">
          <h3>Lose Streak</h3>
          <div class="stat-icon">
            <img src="../../assets/losestreak.webp" alt="Lose Streak Illustrator">
          </div>
          <p>0</p>
        </div>
        <div class="stat-item card">
          <h3>Achievements</h3>
          <div class="stat-icon">
            <img src="../../assets/achievement.webp" alt="Achievement Illustrator">
          </div>
          <p>0</p>
        </div>
      </div>
      <div class="stats">
      <div class="stat-item card">
        <h3>Win Rate %</h3>
        <div class="stat-icon">
          <img src="../../assets/winrate.webp" alt="Win Rate Illustrator">
        </div>
        <p>0</p>
      </div>
      <div class="stat-item card">
        <h3>Win Streak</h3>
        <div class="stat-icon">
          <img src="../../assets/winstreak.png" alt="Win Streak Illustrator">
        </div>
        <p>0</p>
      </div>
      <div class="stat-item card">
        <h3>Lose Streak</h3>
        <div class="stat-icon">
          <img src="../../assets/losestreak.webp" alt="Lose Streak Illustrator">
        </div>
        <p>0</p>
      </div>
      <div class="stat-item card">
        <h3>Achievements</h3>
        <div class="stat-icon">
          <img src="../../assets/achievement.webp" alt="Achievement Illustrator">
        </div>
        <p>0</p>
      </div>
    </div>
    </div>
  </div>
</div>


        `;
    }
}




