import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Friends");
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
                              <a class="nav-link" href="/profile"><i class="bi bi-person-fill"></i> Profile</a>
                          </li>
                          <li class="nav-item">
                              <a class="nav-link" href="/match-history"><i class="bi bi-easel-fill"></i> Match History</a>
                          </li>

                      </ul>
                  </div>
              </nav>
          </div>
      </div>
  </div>
  <div class="card-friends-list">
  <div class="friends-list">
      <div class="row">
          <div class="col-md-6 col-xl-3">                       
              <div class="card friends">
                  <div class="card-body">
                      <div class="media align-items-center">
                          <span style="background-image: url(https://bootdey.com/img/Content/avatar/avatar5.png)" class="avatar avatar-xl mr-3"></span>
                          <div class="media-body overflow-hidden">
                              <h5 class="card-text mb-0">Erika Whitaker</h5>
                              <p class="card-text text-uppercase text-muted">Uniworld</p>
                              <p class="card-text">
                                  erikawhitaker@uniworld.com<br><abbr title="Phone">P:  </abbr>+1 (911) 484-3333
                              </p>
                              <button type="button" class="btn btn-dark"><i class="bi bi-heartbreak-fill"></i> Unfollow</button>
                          </div>
                      </div><a href="#" class="tile-link"></a>
                  </div>
              </div>
          </div>
          <div class="col-md-6 col-xl-3">                       
              <div class="card friends">
                  <div class="card-body">
                      <div class="media align-items-center">
                          <span style="background-image: url(https://bootdey.com/img/Content/avatar/avatar2.png)" class="avatar avatar-xl mr-3"></span>
                          <div class="media-body overflow-hidden">
                              <h5 class="card-text mb-0">Meyers Swanson</h5>
                              <p class="card-text text-uppercase text-muted">Candecor</p>
                              <p class="card-text">
                                  meyersswanson@candecor.com<br><abbr title="Phone">P:  </abbr>+1 (999) 404-3297
                              </p>
                              <button type="button" class="btn btn-dark"><i class="bi bi-heartbreak-fill"></i> Unfollow</button>
                          </div>
                      </div><a href="#" class="tile-link"></a>
                  </div>
              </div>
          </div>
          <div class="col-md-6 col-xl-3">                       
              <div class="card friends">
                  <div class="card-body">
                      <div class="media align-items-center">
                          <span style="background-image: url(https://bootdey.com/img/Content/avatar/avatar7.png)" class="avatar avatar-xl mr-3"></span>
                          <div class="media-body overflow-hidden">
                              <h5 class="card-text mb-0">Townsend Sloan</h5>
                              <p class="card-text text-uppercase text-muted">Rameon</p>
                              <p class="card-text">
                                  townsendsloan@rameon.com<br><abbr title="Phone">P:  </abbr>+1 (978) 563-2964
                              </p>
                              <button type="button" class="btn btn-dark"><i class="bi bi-heartbreak-fill"></i> Unfollow</button>
                          </div>
                      </div><a href="#" class="tile-link"></a>
                  </div>
              </div>
          </div>
          <div class="col-md-6 col-xl-3">                       
              <div class="card friends">
                  <div class="card-body">
                      <div class="media align-items-center">
                          <span style="background-image: url(https://bootdey.com/img/Content/avatar/avatar1.png)" class="avatar avatar-xl mr-3"></span>
                          <div class="media-body overflow-hidden">
                              <h5 class="card-text mb-0">Millicent Henry</h5>
                              <p class="card-text text-uppercase text-muted">Balooba</p>
                              <p class="card-text">
                                  millicenthenry@balooba.com<br><abbr title="Phone">P:  </abbr>+1 (863) 585-3988
                              </p>
                              <button type="button" class="btn btn-dark"><i class="bi bi-heartbreak-fill"></i> Unfollow</button>
                          </div>
                      </div><a href="#" class="tile-link"></a>
                  </div>
              </div>
          </div>
      </div>
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




