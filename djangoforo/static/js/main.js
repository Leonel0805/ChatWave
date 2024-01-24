// websocket 

const RoomId = JSON.parse(document.getElementById('json-roomid').textContent);
const UserHost = JSON.parse(document.getElementById('json-userhost').textContent);
const chatContainer = document.getElementById('room-chat-contenedor');


console.log('Valor de RoomId:', RoomId);
console.log('valor:', UserHost);

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + RoomId + '/'
);

chatSocket.onmessage = function (e) {
    console.log('onmessage')
}

chatSocket.onclose = function (e) {
    console.log('onclose')
}

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)

    if (data.username == UserHost) {
        document.querySelector('#chat-body-room').innerHTML +=        
        `  
        <div class="row message-1">
            <div class="col">
                ${data.message}
            </div>
        </div>
        `;
    } else {
        document.querySelector('#chat-body-room').innerHTML += `
            <div class="row message-2">
                <div class="col">
                    ${data.username} : ${data.message}
                </div>
            </div>
        `;
    }
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        console.log('Botón de envío clickeado');

        document.querySelector('#chat-message-button').click();
    }
};

document.querySelector('#chat-message-button').onclick = function (e) {
    e.preventDefault()

    console.log('boton apretado');
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    if (chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({
            'type': 'message_chat',
            'message': message,
            'username': UserHost,
            'room': RoomId
        }));
    } else {
        console.error('La conexión WebSocket no está abierta.');
    }

    messageInputDom.value = '';
    return false
}



console.log(chatContainer)
