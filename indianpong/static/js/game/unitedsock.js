const roomName = "default";
//export const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');
export const socket = new WebSocket("ws://" + window.location.host + "/ws/pong/" + roomName + "/");