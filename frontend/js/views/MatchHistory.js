import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Match History");
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
      <div class="row mt-4" style="margin-bottom:5px">
          <div class="col">
              <nav class="navbar navbar-expand-lg navbar-light bg-light rounded">
                  <!-- Navbar Marka -->
                  <!-- Navbar Toggle Butonu -->
                  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                      <span class="navbar-toggler-icon"></span>
                  </button>
                  <!-- Navbar Menü -->
                  <div class="collapse navbar-collapse" id="navbarNav">
                      <ul class="navbar-nav ml-auto">
                          <li class="nav-item">
                              <a class="nav-link" href="/profile"><i class="bi bi-person"></i> Profile</a>
                          </li>
                          <li class="nav-item">
                              <a class="nav-link" href="/friends"><i class="bi bi-people-fill"></i> Friends</a>
                          </li>

                      </ul>
                  </div>
              </nav>
          </div>
      </div>
  </div>
</div>
    <div class="card">
      <div class="match-history">
        <table class="card-table">
          <thead>
            <tr>
              <th>Opponent</th>
              <th>Result</th>
              <th>Score</th>
              <th>Date</th>
          </thead>
          <tbody>
            <tr>
              <td>Aykut Kocaman</td>
              <td>Won</th>
              <td>5-2</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr>
              <td>Aykut Kocaman</td>
              <td class="won">Won</th>
              <td>5-2</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr>
              <td>Aykut Kocaman</td>
              <td class="won">Won</th>
              <td>5-2</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr>
              <td>Aykut Kocaman</td>
              <td class="won">Won</th>
              <td>5-2</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr class="disabled">
              <td>Aykut Kocaman</td>
              <td class="won">Won</th>
              <td>5-2</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr>
              <td>Aykut Kocaman</td>
              <td class="lose">Lose</th>
              <td>2-5</th>
              <td>27-07-2024-16:53</td>
            </tr>
            <tr>
             <td>Aykut Kocaman</td>
             <td class="lose">Lose</th>
             <td>2-5</th>
             <td>27-07-2024-16:53</td>
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



        `;
    }
}




