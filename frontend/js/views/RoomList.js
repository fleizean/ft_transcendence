import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
		constructor(params) {
				super(params);
				this.setTitle("Room List");
		}

		async getHtml() {
				return `
				<div class="overlay" id="overlay"></div>
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
								<div class="createRoom-popup" id="createRoom-popup">
									<form class="form" method="post">
										<div class="close-button-container">
											<div class="close-button-create-room">
												<button class="button-close-room" type="button" onclick="closeCreateRoom()">
													<span class="X"></span>
													<span class="Y"></span>
													<div class="close-room">Close</div>
												</button>
								  			</div>
										</div>
										<div class="title">
											You are creating tournament right now!
										</div>
										
										<p class="input-container">
										    <input type="text" placeholder="Room Name" name="text" id="text" class="input-field-createroom">
										</p>

										<div class="checkbox-container">
											<div class="checkbox-wrapper-16">
											  <label class="checkbox-wrapper">
											    <input class="checkbox-input" type="checkbox" id="pongcheckbox" name="gameCheckbox">
											    <span class="checkbox-tile">
											      <span class="checkbox-icon">
													<svg viewBox="0 0 256 256" fill="none" height="192" width="192" xmlns="http://www.w3.org/2000/svg">
													  <rect fill="none" height="256" width="256"></rect>

													  <!-- Pingpong Raketleri -->
													  <rect x="30" y="80" width="20" height="80" fill="currentColor" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" stroke="none"></rect>
													  <rect x="206" y="80" width="20" height="80" fill="currentColor" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" stroke="none"></rect>

													  <!-- Pingpong Topu -->
													  <circle cx="128" cy="128" r="12" fill="currentColor" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" stroke="none"></circle>

													  <!-- Pingpong Tahtası -->
													  <line x1="16" y1="128" x2="240" y2="128" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" stroke="currentColor" fill="none"></line>
													</svg>
											      </span>
											      <span class="checkbox-label">Pong Game</span>
											    </span>
											  </label>
											</div>

											<div class="checkbox-wrapper-16">
											  <label class="checkbox-wrapper">
											    <input class="checkbox-input" type="checkbox" id="rpscheckbox" name="gameCheckbox">
											    <span class="checkbox-tile">
											      <span class="checkbox-icon">
												  <svg fill="#000000" width="256px" height="256px" viewBox="0 0 24 24" id="scissors-3" data-name="Flat Color" xmlns="http://www.w3.org/2000/svg" class="icon flat-color"><path id="primary" d="M20.6,16.51h0a4.19,4.19,0,0,0-2.35-2.31,3,3,0,0,0-2.42.11,3.09,3.09,0,0,0-1.14,1l-1.59-3.5,3.81-8.38a1,1,0,1,0-1.82-.82L12,9.38,8.91,2.59a1,1,0,0,0-1.82.82l3.81,8.38-1.59,3.5a3.09,3.09,0,0,0-1.14-1h0a3,3,0,0,0-2.42-.11A4.19,4.19,0,0,0,3.4,16.51a3.92,3.92,0,0,0,1.43,5.18A2.91,2.91,0,0,0,6.15,22a3.24,3.24,0,0,0,1.1-.2,4.17,4.17,0,0,0,2.34-2.31L12,14.21l2.41,5.28a4.17,4.17,0,0,0,2.34,2.31,3.24,3.24,0,0,0,1.1.2,2.91,2.91,0,0,0,1.32-.31A3.92,3.92,0,0,0,20.6,16.51ZM7.77,18.68h0a2.2,2.2,0,0,1-1.2,1.23,1,1,0,0,1-.83,0,2,2,0,0,1-.5-2.59,2.28,2.28,0,0,1,1.21-1.23A1.19,1.19,0,0,1,6.85,16a1,1,0,0,1,.42.1A2,2,0,0,1,7.77,18.68ZM18.28,19.9a1,1,0,0,1-.84,0,2.23,2.23,0,0,1-1.2-1.23h0a2,2,0,0,1,.49-2.59,1,1,0,0,1,.84,0,2.28,2.28,0,0,1,1.21,1.23A2,2,0,0,1,18.28,19.9Z" style="fill: rgb(0, 0, 0);"></path></svg>





											      </span>
											      <span class="checkbox-label">RPS Game</span>
											    </span>
											  </label>
											</div>
										</div>

										<div class="clash-private-popup_button-container"> 
											<a class="popup-button">LET'S START</a> 
										</div>

									</form>
								</div>
								<h3 class="pong-game-text">Room List</h3>
								<div class="game-room-buttons">
										<button class="leave-button" onclick="activateCreateRoom()" type="button">Create Tournament</button>
								</div>
								<div class="room-wrapper">
									<div class="room-list-container">
										<div class="room-list-box rps">
											<div class="room rps">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box pong">
											<div class="room pong">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box rps">
											<div class="room rps">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box pong">
											<div class="room pong">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box rps">
											<div class="room rps">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box pong">
											<div class="room pong">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box rps">
											<div class="room rps">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
									<div class="room-list-container">
										<div class="room-list-box pong">
											<div class="room pong">
												<div class="room-info-wrapper">
													<div class="room-hover-title">
														#1 - Finn
													</div>
													<div class="room-hover-subtitle">
														7/8
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								
						</div>
					</div>
				`
		}
}