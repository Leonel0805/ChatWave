console.log('hola desde js')

console.log('room-chat-users-container')

const iconBoton = document.getElementById('bi-people')
const divHidden = document.getElementById('room-chat-users-container')
console.log(divHidden)

iconBoton.onclick = function(){
    if (divHidden.style.display === 'none' || divHidden.style.display === ''){
        divHidden.style.display = 'block';
    }else{
        divHidden.style.display = 'none';

    }
}
