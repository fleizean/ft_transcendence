import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Search");
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
            <!-- Arama kutusu ve butonu -->
            <div class="search-container">
                <input type="text" placeholder="Email or Nickname Search..." class="search-input">
                <button class="search-button"><i class="bi bi-search"></i></button>
            </div>
            <div class="card-container-wrapper">
              <div class="card-container">
              	<span class="pro">1ST</span>
                <a href="#" class="go-profile"><img class="round" src="https://randomuser.me/api/portraits/women/79.jpg" alt="user" /></a>              	
				<h3>Ricky Park</h3>
              	<h6>New York</h6>
              	<p>User interface designer and <br/> front-end developer</p>
              	<div class="buttons">
              		<button class="primary">Message</button>
              		<button class="primary ghost">Add Friends</button>
              	</div>
              	<div class="skills">
              		<h6>Skills</h6>
              		<ul>
              			<li>UI / UX</li>
              			<li>Front End Development</li>
              			<li>HTML</li>
              			<li>CSS</li>
              			<li>JavaScript</li>
              			<li>React</li>
              			<li>Node</li>
              		</ul>
              	</div>
              </div>
              <div class="card-container">
              	<span class="pro">2ST</span>
              	<a href="#" class="go-profile"><img class="round" src="https://randomuser.me/api/portraits/women/79.jpg" alt="user" /></a>
              	<h3>Ricky Park</h3>
              	<h6>New York</h6>
              	<p>User interface designer and <br/> front-end developer</p>
              	<div class="buttons">

              		<button class="primary">Message</button>
              		<button class="primary ghost">Add Friends</button>
              	</div>
              	<div class="skills">
              		<h6>Skills</h6>
              		<ul>
              			<li>UI / UX</li>
              			<li>Front End Development</li>
              			<li>HTML</li>
              			<li>CSS</li>
              			<li>JavaScript</li>
              			<li>React</li>
              			<li>Node</li>
              		</ul>
              	</div>
              </div>
            </div>
          </div>
        </div>
      </div>
        `
    }
}