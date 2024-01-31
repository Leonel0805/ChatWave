function hola(){
    alert('Hola desde alerts.js');
}


let botones = document.querySelectorAll('.buttonDelete');
let inputValues = document.querySelectorAll('.inputValue');
let formDeleteID = document.getElementsByClassName('form-delete');
console.log(inputValues);
console.log(formDeleteID);

for (let i=0; i < botones.length; i++){

    botones[i].onclick = function(){
        let confirmacion = window.confirm('Deseas eliminar esta sala?');

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

