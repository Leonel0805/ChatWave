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
    
}

// Disconnect
chatSocket.onclose = function (e) {
    console.log('onclose');
}

// Send Message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data['type'] == 'user_list_room_connect'){
        console.log('userlist_room++++++++++++++++++++++++++++')
        let users = data.message.connected_users

        // reseteamos nuestro ul
        const UserElement = document.getElementById('user-list');
        UserElement.textContent = '';

        for (let i = 0; i < users.length; i++) {
            let username = users[i].username;
       
            let newUser = document.createElement('li');
            newUser.className = 'room-chat-user';
            newUser.textContent = username;
            UserElement.appendChild(newUser);
            }
        
    }

    else if(data['type'] == 'message_chat') {

        console.log('mensaje recibido desde el servidor')
        
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


