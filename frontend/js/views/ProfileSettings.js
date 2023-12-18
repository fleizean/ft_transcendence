import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile Settings");
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
                          <!-- "Edit Profile" Linki -->
                          <li class="nav-item">
                              <a class="nav-link" href="/profile"><i class="bi bi-person"></i> Profile</a>
                          </li>
                          <!-- "Match History" Linki -->
                          <li class="nav-item">
                              <a class="nav-link" href="/match-history"><i class="bi bi-easel-fill"></i> Match History</a>
                          </li>
                      </ul>
                  </div>
              </nav>
          </div>
      </div>
  </div>
    <div class="card">
      <div class="row">
      <!-- Left Sidebar -->
      <div class="col-md-3">
          <nav class="navbar navbar-expand-lg navbar-light bg-light rounded">
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#profileNavbar"
                  aria-controls="profileNavbar" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="profileNavbar">
                  <ul class="navbar-nav flex-column">
                      <li class="nav-item">
                          <a class="nav-link" href="javascript:void(0);" onclick="displaySection('editProfile')"><i class="bi bi-pencil-fill"></i> Edit Profile</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link" href="javascript:void(0);" onclick="displaySection('changePassword')"><i class="bi bi-lock-fill"></i> Change Password</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link" href="javascript:void(0);" onclick="showAddSocialSection()"><i class="bi bi-bookmark-fill"></i> Add Socials</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link" href="javascript:void(0);" onclick="showCloseAccountSection()"><i class="bi bi-door-closed-fill"></i> Close Account</a>
                      </li>
                  </ul>
              </div>
          </nav>
      </div>

    <!-- Edit Profile Content -->

    <div class="col-xl-9">
        <!-- Change Photo Section -->

        <!-- Edit Profile Form -->
        <section id="editProfile">
            <form id="editProfileForm">
                  <div class="profile-pic-container">
                  <label for="fileInput" class="profile-pic-label">
                    <img src="../../assets/profile/profilephoto.jpeg" alt="Profile Picture" class="profile-pic">
                    <div class="change-image-overlay">
                      <span class="bi bi-image-fill"></span>
                      <span class="change-image-text">Change Image</span>
                    </div>
                  </label>
                  <input type="file" id="fileInput" class="file-input">
                </div>

                <!-- Username textbox -->
                <div class="mb-3">
                    <label class="small mb-1" for="inputUsername">Username (how your name will appear to other users on the site)</label>
                    <input class="form-control" id="inputUsername" type="text" value="eyagiz">
                </div>

                <!-- Email textbox -->
                <div class="mb-3">
                    <label class="small mb-1" for="inputEmail">Email</label>
                    <input class="form-control" id="inputEmail" type="text" value="nsyagz@gmail.com" type="email">
                </div>

                <!-- Firstname textbox -->
                <div class="row gx-3 mb-3">
                    <!-- Form Group (first name)-->
                    <div class="col-md-6">
                        <label class="small mb-1" for="inputFirstName">First name</label>
                        <input class="form-control" id="inputFirstName" type="text" value="Fatih">
                    </div>
                    <!-- Form Group (last name)-->
                    <div class="col-md-6">
                        <label class="small mb-1" for="inputLastName">Last name</label>
                        <input class="form-control" id="inputLastName" type="text" value="Terim">
                    </div>
                </div>
                <!-- Email address textbox -->
                <div class="row gx-3 mb-3">
                    <!-- Form Group (phone number)-->
                    <div class="col-md-6">
                        <label class="small mb-1" for="inputPhone">Phone number</label>
                        <input class="form-control" id="inputPhone" type="tel" value="(545) 411 9245">
                    </div>
                    <!-- Form Group (birthday)-->
                    <div class="col-md-6">
                        <label class="small mb-1" for="inputBirthday">Birthday</label>
                        <input class="form-control" id="inputBirthday" type="text" name="birthday" value="27/07/2002">
                    </div>
                </div>
                <!-- Submit button -->
                <button type="submit" class="btn btn-success">Save Changes</button>
            </form>
        </section>

        <!-- Change Password Section -->
        <section id="changePassword">
            <!-- Your code for changing password goes here -->
            <form id="changePasswordForm">
                    
                    <div class="mb-3 position-relative">
                        <label class="small mb-1" for="currentPassword">Current Password</label>
                        <div class="input-group">
                            <input class="form-control" id="currentPassword" type="password" required>
                            <button class="btn btn-outline-secondary" type="button" onclick="togglePasswordVisibility('currentPassword')">
                                <i class="bi bi-eye"></i>
                            </button>
                        </div>
                    </div>

                    <div class="mb-3 position-relative">
                        <label class="small mb-1" for="newPassword">New Password</label>
                        <div class="input-group">
                            <input class="form-control" id="newPassword" type="password" required>
                            <button class="btn btn-outline-secondary" type="button" onclick="togglePasswordVisibility('newPassword')">
                                <i class="bi bi-eye"></i>
                            </button>
                        </div>
                    </div>

                    <div class="mb-3 position-relative">
                        <label class="small mb-1" for="confirmNewPassword">Confirm New Password</label>
                        <div class="input-group">
                            <input class="form-control" id="confirmNewPassword" type="password" required>
                            <button class="btn btn-outline-secondary" type="button" onclick="togglePasswordVisibility('confirmNewPassword')">
                                <i class="bi bi-eye"></i>
                            </button>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary"><i class="bi bi-lock-fill"></i> Change Password</button>
                </form>
        </section>

        <section id="addSocial">
            <!-- Your code for add socials goes here -->
        </section>

        <section id="closeAccount">
            <!-- Your code for close account goes here -->
        </section>
                </div>
            </div>
        </div>



        `;
    }
}




