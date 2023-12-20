import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Achievements");
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
                              <a class="nav-link" href="/match-history"><i class="bi bi-easel-fill"></i> Match History</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link" href="/friends"><i class="bi bi-people-fill"></i> Friends</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link" href="/achievements"><i class="bi bi-magic"></i> Achievements</a>
                          </li>
                      </ul>
                  </div>
              </nav>
          </div>
      </div>
  </div>
    <div class="card">
            <div class="achievements-container">
            <!-- 1. Achievements Card -->
            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 1</h4>
                    <p>Here is the description of Achievement 1.</p>
                    <p class="achievement-date">Achieved on: January 1, 2023</p>
                </div>
            </div>

            <!-- 2. Achievements Card -->
            <div class="card achievement-card">
                    <div class="achievement-img">
                        <img src="./assets/achievements/award.png" alt="Achievement 3">
                    </div>
                    <div class="achievement-details">
                        <h4>Achievement 2</h4>
                        <p>Here is the description of Achievement 2.</p>
                        <p class="achievement-date">Achieved on: February 15, 2023</p>
                    </div>
            </div>

            <!-- 3. Achievements Card -->
            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                    <div class="achievement-details">
                        <h4>Achievement 3</h4>
                        <p>Here is the description of Achievement 3.</p>
                        <p class="achievement-date">Achieved on: March 22, 2023</p>
                    </div>
            </div>

            <!-- 4. Achievements Card -->
            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <!-- 4. Achievements Card -->
            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <!-- 4. Achievements Card -->
            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>

            <div class="card achievement-card">
                <div class="achievement-img">
                    <img src="./assets/achievements/award.png" alt="Achievement 3">
                </div>
                <div class="achievement-details">
                    <h4>Achievement 4</h4>
                    <p>Here is the description of Achievement 4.</p>
                    <p class="achievement-date">Achieved on: April 5, 2023</p>
                </div>
            </div>
            
        </div>
        <nav aria-label="...">
          <ul class="pagination pagination-sm d-flex justify-content-center">
            <li class="page-item disabled">
              <a class="page-link" href="#" tabindex="-1">1</a>
            </li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
          </ul>
        </nav>
    </div>
   


        `;
    }
}




