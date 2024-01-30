import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Game");
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
      <li><a href="/about-us" data-link><i class="bi bi-4-square-fill"></i>About Us</a></li>
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

        <div class="left-card">
            <table class="custom-table">
                
              <thead>
                  <tr>
                      <th>Name</th>
                      <th>Actions</th>
                      <!-- Diğer sütunlar... -->
                  </tr>
              </thead>
              <tbody>
                  <!-- Burada liste elemanları döngü ile eklenir -->
                  <tr>
                      <td><img src="https://www.trtspor.com.tr/resimler/260000/260382.jpg"> ardaturan</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://img.a.transfermarkt.technology/portrait/big/1061-1612175084.jpeg?lm=1"> aykutkocaman</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://cdn.ntvspor.net/17b65e4cfb844414bc1f37abbbca62f2.jpg?mode=crop&w=940&h=626"> ersunyanal</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="../../assets/profile/profilephoto.jpeg"> fatihterim</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://cdn.ntvspor.net/17b65e4cfb844414bc1f37abbbca62f2.jpg?mode=crop&w=940&h=626"> ersunyanal</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://img.a.transfermarkt.technology/portrait/big/7237-1595580698.jpg?lm=1"> sarioglu</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://cdn.ntvspor.net/f26901d08c0c436aab85737d8625c5c7.jpg?mode=crop&w=940&h=626"> belezoglu</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/bltf9f319eb4fa8a1e6/60dbc05963584e0ecae47963/6932614169eadb875c001f02448a33658136f9c3.jpg?auto=webp&format=pjpg&width=3840&quality=60"> oburuk</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                   <tr>
                      <td><img src="https://img.a.transfermarkt.technology/portrait/big/801-1477746457.jpg?lm=1"> hkaraman</td>
                      <td><button type="button" class="btn btn-outline-success"><i class="bi bi-plus-circle-fill"></i></button>
                      <button type="button" onclick="setCanvasSize()" class="btn btn-outline-primary"><i class="bi bi-patch-check-fill"></i></button>
                      <button type="button" class="btn btn-outline-danger"><i class="bi bi-x-circle-fill"></i></button></td>
                      <!-- Diğer sütun değerleri... -->
                  </tr>
                  
                  <!-- Diğer liste elemanları... -->
              </tbody>
            </table>
  
            <!-- Pagination Alanı -->
            <div class="pagination">
                <a href="#">&laquo;</a>
                <a href="#">1</a>
                <a href="#">2</a>
                <a href="#">3</a>
                <a href="#">4</a>
                <a href="#">5</a>
                <a href="#">&raquo;</a>
            </div>
        </div>
  
      <!-- Sağ Taraftaki Canvas Alanı -->
      <div class="canvas-container">
          <canvas id="myCanvas"></canvas>
      </div>

      
        `
    }
}