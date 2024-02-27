const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/users_online/');
const UserHost = JSON.parse(document.getElementById('json-authenticated-user').textContent);


chatSocket.onopen = function(e){
    console.log('conexion establecida websocket')
    chatSocket.send(JSON.stringify({
        'type': 'connect_user',
    }));
   
}

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);

    if (data['type'] == 'user_list_connect'){
        console.log('userlist_connect')
        console.log(data.users)

        let users = data.users

        const userCardUrlElements = document.getElementsByClassName('meet-card-url');
        const usernameElements = document.getElementsByClassName('meet-card-username');

        console.log(usernameElements)
        
        for (let i = 0; i < usernameElements.length; i++) {
            const username = usernameElements[i].textContent.trim(); //trim elimina espacio sen blanco principo y final
            const UrlElment = userCardUrlElements[i];


            let userOnline = false;

            for (let j=0; j<users.length; j++){
                // console.log('username', username, 'user', users[j]['username'])
                if(username === users[j]['username']){
                    console.log(`El usuario ${username} esta online`);
                    userOnline = true;
                    break;       
                }
                
            }   
            let newIcon = document.createElement('i');
            if (userOnline) {
                newIcon.className = 'bi bi-circle-fill';
            } else {
                newIcon.className = 'bi bi-circle';
            }

            newIcon.classList.add('custom-bi')
            UrlElment.appendChild(newIcon);
        }   
    }
    else if (data['type']=='user_list_disconnect'){
        console.log('user_llist_disconnect')
        
    }

}