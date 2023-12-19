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
</div>
    <div class="card">
        <div class="row">
            <!-- Sol Sütun (col-lg-4) -->
            <div class="col-lg-4">
                <!-- Profil Kartı -->
                <div class="card mb-4">
                    <!-- Profil Kartı İçeriği -->
                    <span class="pro-profile"><i class="bi bi-award-fill"></i> 1ST IN RANKINGS</span>
                    <div class="card-body text-center">
                        <!-- Avatar -->
                        <img src="../../assets/profile/profilephoto.jpeg"
                            alt="avatar" class="rounded-circle img-fluid" style="width: 150px;">
                        <!-- İsim -->
                        
                        <h5 class="my-3">Fatih Terim</h5>
                        <!-- Meslek -->
                        <p class="text-muted mb-1">Full Stack Developer</p>
                        <!-- Konum -->
                        <p class="text-muted mb-4">Bay Area, San Francisco, CA</p>
                        <!-- Takip ve İstatistik Butonları -->
                        <div class="d-flex justify-content-center mb-2">
                            <button type="button" class="btn btn-danger"><i class="bi bi-heart-fill"></i> Follow</button>
                            <button type="button" class="btn btn-dark" style="display:none"><i class="bi bi-heartbreak-fill"></i> Unfollow</button>
                            <a href="/profile-stats" class="btn btn-outline-info ms-1">
                                <i class="bi bi-bar-chart-fill"></i> Stats
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Sosyal Medya ve Website Bilgileri -->
                <div class="card mb-4 mb-lg-0">
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush rounded-3">
                            <!-- Website -->
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="bi bi-globe"></i>
                                <p class="mb-0">www.indianpong.com</p>
                            </li>
                            <!-- GitHub -->
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="bi bi-github" style="color: #333333;"></i>
                                <p class="mb-0">fleizean</p>
                            </li>
                            <!-- Twitter -->
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="bi bi-twitter" style="color: #55acee;"></i>
                                <p class="mb-0">@test</p>
                            </li>
                            <!-- Instagram -->
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="bi bi-instagram" style="color: #ac2bac;"></i>
                                <p class="mb-0">fleizean</p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- Sağ Sütun (col-lg-8) -->
            <div class="col-lg-8">
                <!-- Profil Bilgileri -->
                <div class="card mb-4">
                    <div class="card-body">
                        <!-- İsim -->
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Full Name</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">Fatih Terim</p>
                            </div>
                        </div>
                        <hr>
                        <!-- Email -->
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Email</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">example@example.com</p>
                            </div>
                        </div>
                        <hr>
                        <!-- Telefon -->
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Phone</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">(097) 234-5678</p>
                            </div>
                        </div>
                        <hr>
                        <!-- Mobil -->
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Mobile</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">(098) 765-4321</p>
                            </div>
                        </div>
                        <hr>
                        <!-- Adres -->
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Address</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">Bay Area, San Francisco, CA</p>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Proje Durumu Kartları -->
                <div class="row">
                    <!-- Sol Proje Kartı -->
                    <div class="col-md-6">
                        <div class="card mb-4 mb-md-0">
                            <div class="card-body">
                                <!-- Proje Durumu Başlığı -->
                                <p class="mb-4"><span class="text-primary font-italic me-1">Fatih Terim </span> Rank</p>
                                <div class="rank-img">
                                    <img src="../../assets/ranks/challenger.png" alt="Challenger Rank">
                                    <h4 class="rank-h4">Challenger</h4>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Sağ Proje Kartı -->
                    <div class="col-md-6">
                        <div class="card mb-4 mb-md-0">
                            <div class="card-body">
                                <!-- Proje Durumu Başlığı -->
                                <p class="mb-4"><span class="text-primary font-italic me-1">last 5</span> Followers</p>
                                    <div class="follower">
                                        <a href=""><img src="../../assets/profile/c1.jpg"></a>
                                        <span class="displayname">test</span>
                                    </div>

                                    <div class="follower">
                                        <a href=""><img src="../../assets/profile/c2.jpg"></a>
                                        <span class="displayname">test2</span>
                                    </div>

                                    <div class="follower">
                                        <a href=""><img src="../../assets/profile/c3.jpg"></a>
                                        <span class="displayname">test3</span>
                                    </div>

                                    <div class="follower">
                                        <a href=""><img src="../../assets/profile/c4.jpg"></a>
                                        <span class="displayname">test4</span>
                                    </div>

                                    <div class="follower">
                                        <a href=""><img src="../../assets/profile/c1.jpg"></a>
                                        <span class="displayname">test5</span>
                                    </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>



        `;
    }
}




