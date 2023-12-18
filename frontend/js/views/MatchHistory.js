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
          <li><a href="/game" data-link><i class="bi bi-play-circle-fill"></i>Game</a></li>
          <li><a href="/chat" data-link><i class="bi bi-chat-fill"></i>Chat</a></li>
          <li><a href="/rankings" data-link><i class="bi bi-bar-chart-fill"></i>Rankings</a></li>
          <li><a href="/search" data-link><i class="bi bi-binoculars-fill"></i>Search</a></li>
          <li class="profile-menu">
            <div class="profile-image">
              <img src="../../assets/profile/profilephoto.jpeg" alt="Profile Image" width="48" height="48">
            </div>
            <div class="profile-submenu">
              <a href="/profile" data-link><i class="bi bi-person-fill"></i>Profile</a>
              <a href="/logout" data-link><i class="bi bi-box-arrow-right"></i>Logout</a>
            </div>
          </li>
        </ul>
        <div class="burger-menu">&#9776;</div>
      </nav>

      <div class="container-top">
      <!-- "Edit Profile" ve "Match History" Navbar -->
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
                          <!-- "Profile Settings" Linki -->
                          <li class="nav-item">
                              <a class="nav-link" href="/profile-settings"><i class="bi bi-gear-fill""></i> Profile Settings</a>
                          </li>
                      </ul>
                  </div>
              </nav>
          </div>
      </div>
  </div>
</div>
    <div class="card">
        
    </div>



        `;
    }
}




