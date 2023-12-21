import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Game");
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
      <li><a href="/pong-game" data-link><i class="bi bi-play-circle-fill"></i>Pong Game</a></li>
      <li><a href="/rps-game" data-link><i class="bi bi-scissors"></i>RPS Game</a></li>
      <li><a href="/game-stats" data-link><i class="bi bi-pie-chart-fill"></i>Game Stats</a></li>
      <li><a href="/rankings" data-link><i class="bi bi-bar-chart-fill"></i>Rankings</a></li>
      <li><a href="/search" data-link><i class="bi bi-binoculars-fill"></i>Search</a></li>
      <li class="profile-menu">
        <div class="profile-image">
          <img src="../../assets/profile/profilephoto.jpeg" alt="Profile Image" width="48" height="48">
        </div>
        <div class="profile-submenu">
          <a href="/profile" data-link><i class="bi bi-person-fill"></i>Profile</a>
          <a href="/profile-settings" data-link><i class="bi bi-gear-fill"></i>Settings</a> 
          <a href="/logout" data-link><i class="bi bi-box-arrow-right"></i>Logout</a>
        </div>
      </li>
    </ul>
    <div class="burger-menu">&#9776;</div>
  </nav>

          <div class="container-top">
            <div class="card">
              <h3 class="pong-game-text">Welcome to Tournament</h3>
              <div class="custom-text">
                You can play with the AI and improve yourself without reflecting it in your stats, as if you were just warming up. If you want to play with a real person, consider the other option, remember that if we don't find someone to match you within 5 minutes, the match will be canceled. Good luck before I forget!
              </div>

              <div class="ai-btn">
                <div class="ponggamebtn-ai">Play With AI <i class="bi bi-robot"></i></div>
              </div>
              <div class="opponent-btn">
                <div class="ponggamebtn">Search Opponent <i class="bi bi-person-arms-up"></i></div>
              </div>
            </div>
          </div>
        `
    }
}