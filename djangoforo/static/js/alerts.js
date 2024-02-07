function hola(){
    console.log('Hola desde alerts.js');
}

let botones = document.querySelectorAll('.boton-rooms-eliminar');
let inputValues = document.querySelectorAll('.inputValue');
let formDeleteID = document.getElementsByClassName('form-delete');

let RoomsTitle = document.getElementsByClassName('room-card-title');


console.log(formDeleteID)
console.log(botones)
console.log(RoomsTitle)



for (let i=0; i < botones.length; i++){

    botones[i].onclick = function(){
        let confirmacion = window.confirm(`Deseas eliminar ${RoomsTitle[i].textContent}?`);

        // Verifica la respuesta del usuario
        if (confirmacion) {
            // El usuario ha confirmado, puedes realizar acciones de eliminación u otras operaciones
            inputValues[i].value = 'delete'
        } else {
            // El usuario ha cancelado la acción
            inputValues[i].value = ''

        }
    };
}

for (let input of inputValues){
    console.log(input.name);
}

hola();
