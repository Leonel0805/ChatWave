const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/users_online/');
const UserHost = JSON.parse(document.getElementById('json-authenticated-user').textContent);


console.log(UserHost)
chatSocket.onopen = function(e){
    console.log('conexion establecida websocket')
}

chatSocket.onmessage = function(e){

}