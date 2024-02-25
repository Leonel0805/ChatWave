// websocket 

const RoomId = JSON.parse(document.getElementById('json-roomid').textContent);
const UserHost = JSON.parse(document.getElementById('json-authenticated-user').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/' + RoomId + '/');

// ngrok
// const chatSocket = new WebSocket('wss://' + window.location.host + '/ws/' + RoomId + '/');

const chatContainer = document.getElementById('chat-body-room');


// Connect
chatSocket.onopen = function (e) {
    console.log('Conexión establecida');
    
    chatSocket.send(JSON.stringify({
        'type': 'connect_user',
        'username': UserHost,
    }));
   

}

// Disconnect
chatSocket.onclose = function (e) {
    console.log('onclose');
}

// Send Message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data['type'] == 'user_list'){
        console.log('userlist')
        console.log(data.users)
    }

    else {
        
        // Crear un nuevo elemento de mensaje
        const messageElement = document.createElement('div');
        messageElement.classList.add('container-message', data.username == UserHost ? 'container-message-1' : 'container-message-2'); //le agregamos una class

        //creamos la col para messageElement
        const colElement = document.createElement('div');
        colElement.classList.add(data.username == UserHost ? 'message-1' : 'message-2');

        //configuramos el message dentro de col
        colElement.textContent = data.username == UserHost ? data.message : `${data.username}: ${data.message}`;


        messageElement.appendChild(colElement);
        chatContainer.appendChild(messageElement);


        //desplazamiento de scroll
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

};


document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        console.log('Botón de envío clickeado');

        document.querySelector('#chat-message-button').click();
    }
};

document.querySelector('#chat-message-button').onclick = function (e) {
    e.preventDefault()

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



