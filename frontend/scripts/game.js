// function startConnection() {
//     const roomName = '1'; // You may change this to a dynamic value if needed
//     const socket = new WebSocket('ws://127.0.0.1:8000/ws/game/');

//     socket.onopen = function() {
//         console.log('Connection is open');
//         socket.send(JSON.stringify({ 'message': 'Hello Server' }));
//     }

//     socket.onmessage = function(event) {
//         console.log('Message from server: ', event.data);
//     }

//     socket.onclose = function() {
//         console.log('Connection is closed');
//     }
// }