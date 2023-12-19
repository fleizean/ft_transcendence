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
          <li><a href="/game" data-link><i class="bi bi-play-circle-fill"></i>Game</a></li>
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
                <div class="rankings-card">
                    <div class="main-center">
                    <main>
                      <div id="header">
                        <h1>Ranking</h1>
                        <button class="share">
                          <i class="bi bi-share-fill"></i>
                        </button>
                      </div>
                      <div id="leaderboard">
                        <div class="ribbon"></div>
                        <table>
                          <tr>
                            <td class="number">1</td>
                            <td class="name">Lee Taeyong</td>
                            <td class="points">
                              258.244 <img class="gold-medal" src="https://github.com/malunaridev/Challenges-iCodeThis/blob/master/4-leaderboard/assets/gold-medal.png?raw=true" alt="gold medal"/>
                            </td>
                          </tr>
                          <tr>
                            <td class="number">2</td>
                            <td class="name">Mark Lee</td>
                            <td class="points">258.242</td>
                          </tr>
                          <tr>
                            <td class="number">3</td>
                            <td class="name">Xiao Dejun</td>
                            <td class="points">258.223</td>
                          </tr>
                          <tr>
                            <td class="number">4</td>
                            <td class="name">Qian Kun</td>
                            <td class="points">258.212</td>
                          </tr>
                          <tr>
                            <td class="number">5</td>
                            <td class="name">Johnny Suh</td>
                            <td class="points">258.208</td>
                          </tr>
                        </table>
                        
                      </div>
                    </main>
                </div>


                </div>
	        </div>

        `;
    }
}




