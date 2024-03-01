const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/users_online/');
const UserHost = JSON.parse(document.getElementById('json-authenticated-user').textContent);


chatSocket.onopen = function(e){
    console.log('conexion establecida websocket')

}

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log('onmessage', data);
    console.log('type', data['type']);

    if (data['type'] == 'user_list_connect'){
        console.log('userlist_connect')
        console.log(data.message)

        let users = data.message.connected_users
        console.log(users)

        const userCardUrlElements = document.getElementsByClassName('meet-card-url');
        const usernameElements = document.getElementsByClassName('meet-card-username');

        console.log(usernameElements)
        
        for (let i = 0; i < usernameElements.length; i++) {
            const UrlElment = userCardUrlElements[i];
            const username = usernameElements[i].textContent.trim(); //trim elimina espacio sen blanco principo y final

            let userOnline = false;

            for (let j=0; j<users.length; j++){
                // console.log('username', username, 'user', users[j]['username'])
                if(username === users[j]['username']){
                    console.log(`El usuario ${username} esta online`);
                    userOnline = true;
                    break;       
                }
                
            }   

            let IconExist = UrlElment.querySelector('i')

            if (IconExist){
                if (userOnline) {
                    IconExist.className = 'bi bi-circle-fill';
                } else {
                    IconExist.className = 'bi bi-circle';
                }
    
            }else{
                let newIcon = document.createElement('i');
                newIcon.className = userOnline ? 'bi bi-circle-fill' : 'bi bi-circle';
                UrlElment.appendChild(newIcon);
            }
    

        }   
    }

}