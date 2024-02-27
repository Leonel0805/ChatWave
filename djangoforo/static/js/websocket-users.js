const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/users_online/');
const UserHost = JSON.parse(document.getElementById('json-authenticated-user').textContent);


chatSocket.onopen = function(e){
    console.log('conexion establecida websocket')

}

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);

    if (data['type'] == 'user_list'){
        console.log('userlist')
        console.log(data.users)
    }

}