const iconBoton = document.getElementById('bi-people')
const divHidden = document.getElementById('room-chat-users-container')

iconBoton.onclick = function(){
    if (divHidden.style.display === 'none' || divHidden.style.display === ''){
        divHidden.style.display = 'block';
    }else{
        divHidden.style.display = 'none';

    }
}
