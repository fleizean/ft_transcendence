import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile Stats");
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
                            <!-- "Match History" Linki -->
                            <li class="nav-item">
                                <a class="nav-link" href="/profile"><i class="bi bi-person"></i> Profile</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/match-history"><i class="bi bi-easel-fill"></i> Match History</a>
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
        <div class="card">
        <div class="row">
        <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-blue order-card">
            <div class="card-block">
                <h6 class="m-b-20">Games Played</h6>
                <h2 class="text-right"><i class="bi bi-dice-1-fill"></i><span>50</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">500</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-green order-card">
            <div class="card-block">
                <h6 class="m-b-20">Win Count</h6>
                <h2 class="text-right"><i class="bi bi-trophy-fill"></i><span>486</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">500</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-yellow order-card">
            <div class="card-block">
                <h6 class="m-b-20">Win Streak</h6>
                <h2 class="text-right"><i class="bi bi-emoji-wink-fill"></i><span>486</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">500</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-pink order-card">
            <div class="card-block">
                <h6 class="m-b-20">Lose Streak</h6>
                <h2 class="text-right"><i class="bi bi-emoji-frown-fill"></i><span>486</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">500</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-gold order-card">
            <div class="card-block">
                <h6 class="m-b-20">Win Rate %</h6>
                <h2 class="text-right"><i class="bi bi-award-fill"></i><span>50</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">70</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-navy order-card">
            <div class="card-block">
                <h6 class="m-b-20">Average Game Duration</h6>
                <h2 class="text-right">
                  <i class="bi bi-clock-fill"></i>
                  <span class="big">30</span> <span class="small">min</span>
                  </h2>
              <p class="m-b-0">Achievement Reach<span class="f-right">15 and 30</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-light-green order-card">
            <div class="card-block">
                <h6 class="m-b-20">Average Points Won</h6>
                <h2 class="text-right"><i class="bi bi-star-fill"></i><span>30</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">50</span></p>
            </div>
        </div>
    </div>

    <div class="col-md-4 col-xl-3">
        <div class="card-stat bg-c-purple order-card">
            <div class="card-block">
                <h6 class="m-b-20">Average Points Lost</h6>
                <h2 class="text-right"><i class="bi bi-bucket-fill"></i><span>20</span></h2>
                <p class="m-b-0">Achievement Reach<span class="f-right">50</span></p>
            </div>
        </div>
    </div>
    </div>
        </div>
   



        `;
    }
}




