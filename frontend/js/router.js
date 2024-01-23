import Home from "./views/Home.js";
import Login from "./views/Login.js";
import Dashboard from "./views/Dashboard.js"
import Register from "./views/Register.js"
import Search from "./views/Search.js";
import Rankings from "./views/Rankings.js";
import Profile from "./views/Profile.js";
import MatchHistory from "./views/MatchHistory.js";
import ProfileSettings from "./views/ProfileSettings.js";
import Error404 from "./views/Error404.js";
import Friends from "./views/Friends.js";
import PongGame from "./views/PongGame.js";
import RpsGame from "./views/RpsGame.js";
import Pass2FA from "./views/Pass2FA.js";
import GameRoom from "./views/GameRoom.js";
import RoomList from "./views/RoomList.js";
import GameChart from "./views/GameChart.js";
import Chat from "./views/Chat.js";
import InChat from "./views/InChat.js";
import ForgotPassword from "./views/ForgotPassword.js";
import Pong from "./views/Pong.js";

const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = match => {
    const values = match.result.slice(1);
    const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

    return Object.fromEntries(keys.map((key, i) => {
        return [key, values[i]];
    }));
};

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        { path: "/", view: Home },
        { path: "/login", view: Login },
        { path: "/register", view: Register},
        { path: '/dashboard', view: Dashboard },
        { path: '/pong-game', view: PongGame},
        { path: '/rps-game', view: RpsGame},
        { path: '/search', view: Search},
        { path: '/rankings', view: Rankings},
        { path: '/profile', view: Profile},
        { path: '/game-room', view: GameRoom},
        { path: '/room-list', view: RoomList},
        { path: '/game-chart', view: GameChart},
        { path: '/forgot-password', view: ForgotPassword},
        { path: '/chat', view: Chat},
        { path: '/in-chat', view: InChat},
        { path: '/in-game', view: Pong},
        { path: '/pass2fa', view: Pass2FA},
        { path: '/profile-settings', view: ProfileSettings},
        { path: '/match-history', view: MatchHistory},
        { path: '/friends', view: Friends},
    ];

    // Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            result: location.pathname.match(pathToRegex(route.path))
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);

    if (!match) {
        match = {
            route: routes.find(route => route.path === '/404'), // Eğer hiçbir yol eşleşmezse 404 sayfasına yönlendir
            result: [location.pathname]
        };
    }

    const view = new match.route.view(getParams(match));

    document.querySelector("#app").innerHTML = await view.getHtml();
};

window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
    });

    router();
});