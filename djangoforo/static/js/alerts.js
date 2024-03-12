let botones = document.querySelectorAll('.boton-rooms-eliminar');
let inputValues = document.querySelectorAll('.inputValue');
let formDeleteID = document.getElementsByClassName('form-delete');

let RoomsTitle = document.getElementsByClassName('room-card-title');

// console.log(formDeleteID)
// console.log(botones)
// console.log(RoomsTitle)


for (let i=0; i < botones.length; i++){

    botones[i].onclick = function(){
        let confirmacion = window.confirm(`Deseas eliminar ${RoomsTitle[i].textContent}?`);

        // Si confirma eliminar
        if (confirmacion) {
            
            inputValues[i].value = 'delete'
        } else {
            
            inputValues[i].value = ''

        }
    };
}


