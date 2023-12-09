import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Dashboard");
    }

    async getHtml() {
        return `
        <nav class="navbar">
        <div class="logo-container"><a href="#">
          <div class="logo">
            <img src="../../assets/logo.png" alt="IndianPong Logo" width="48" height="48">
            IndianPong
          </div></a>
      </div>
        <ul class="nav-links">
          <li><a href="#"><i class="bi bi-house-door-fill"></i>Dashboard</a></li>
          <li><a href="#"><i class="bi bi-play-circle-fill"></i>Game</a></li>
          <li><a href="#"><i class="bi bi-chat-fill"></i>Chat</a></li>
          <li><a href="#"><i class="bi bi-heart-fill"></i>Friends</a></li>
          <li><a href="#"><i class="bi bi-binoculars-fill"></i>Search</a></li>
          <li><a href="#"><i class="bi bi-person-fill"></i>Profile</a></li>
        </ul>
        <div class="burger-menu">&#9776;</div>
      </nav>

      <div class="container-top">
          <div class="card">
            <div class="page-rotation">
              <h1>Welcome to IndianPong</h1>
              <p>This is the main content area. You can add your Ping Pong game, chat, and friends sections here.</p>
              <a href="/ping-pong">Ping Pong Game</a>
              <a href="/chat">Chat</a>
              <a href="/friends">Friends</a>
            </div>
            <div class="page-rotation">
              <h1>Welcome to IndianPong</h1>
              <p>This is the main content area. You can add your Ping Pong game, chat, and friends sections here.</p>
              <a href="/ping-pong">Ping Pong Game</a>
              <a href="/chat">Chat</a>
              <a href="/friends">Friends</a>
            </div>
            <div class="page-rotation">
              <h1>Welcome to IndianPong</h1>
              <p>This is the main content area. You can add your Ping Pong game, chat, and friends sections here.</p>
              <a href="/ping-pong">Ping Pong Game</a>
              <a href="/chat">Chat</a>
              <a href="/friends">Friends</a>
            </div>
            <div class="page-rotation">
              <h1>Welcome to IndianPong</h1>
              <p>This is the main content area. You can add your Ping Pong game, chat, and friends sections here.</p>
              <a href="/ping-pong">Ping Pong Game</a>
              <a href="/chat">Chat</a>
              <a href="/friends">Friends</a>
            </div>
            <div class="page-rotation">
              <h1>Welcome to IndianPong</h1>
              <p>This is the main content area. You can add your Ping Pong game, chat, and friends sections here.</p>
              <a href="/ping-pong">Ping Pong Game</a>
              <a href="/chat">Chat</a>
              <a href="/friends">Friends</a>
            </div>
          </div>
        </div>

        `;
    }
}




