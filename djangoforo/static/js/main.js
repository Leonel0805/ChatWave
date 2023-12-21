// websocket 

const RoomId = JSON.parse(document.getElementById('json-roomid').textContent);


console.log('Valor de RoomId:', RoomId);

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + RoomId + '/'
);

chatSocket.onmessage = function (e) {
    console.log('onmessage')
}

chatSocket.onclose = function (e) {
    console.log('onclose')
}