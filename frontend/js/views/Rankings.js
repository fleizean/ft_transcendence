import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Rankings");
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
      <li><a href="/chat" data-link><i class="bi bi-chat-fill"></i>Chat</a></li>
      <li><a href="/pong-game" data-link><i class="bi bi-play-circle-fill"></i>Pong Game</a></li>
	  <li><a href="/rps-game" data-link><i class="bi bi-scissors"></i>RPS Game</a></li>
      <li><a href="/rankings" data-link><i class="bi bi-bar-chart-fill"></i>Rankings</a></li>
      <li><a href="/search" data-link><i class="bi bi-binoculars-fill"></i>Search</a></li>
      <li class="notification-menu">
        <div class="notification-icon">
            <i class="bi bi-bell-fill"></i>
            
        </div>
        <div class="notification-submenu">
        <a href="/test" data-link><i class="bi bi-person-fill"></i>Arda followed you!</a>
        </div>
      </li>
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
            <div class="rankings-card-header">
              <h3 class="rankings-header"> / Rankings</h3>
            </div>
            <div class="rankings">
            <table class="card-rankings-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Users</th>
                  <th>Wins</th>
                  <th>Losses</th>
                  <th>Win Rate</th>
                  <th>Pong Point (PP)</th>
              </thead>
              <tbody>
                <tr>
                  <td class="rank-number">1</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">2</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">3</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">4</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">5</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">6</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td class="rank-number">7</td>
                  <td class="rank-username">fterim</th>
                  <td class="wins">5</th>
                  <td class="losses">0</td>
                  <td class="win-rate">100%</td>
                  <td>60</td>
                </tr>
    
              </tbody>
            </table>
            <nav aria-label="Page navigation example">
              <ul class="pagination">
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                  </a>
                </li>
                <li class="page-item"><a class="page-link" href="#">1</a></li>
                <li class="page-item"><a class="page-link" href="#">2</a></li>
                <li class="page-item"><a class="page-link" href="#">3</a></li>
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                  </a>
                </li>
              </ul>
            </nav>
          </div>
            </div>
	        </div>

        `;
    }
}




