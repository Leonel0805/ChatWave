function hola(){
    alert('Hola desde alerts.js')
}


let botones = document.querySelectorAll('.buttonDelete');
let inputValues = document.querySelectorAll('.inputValue');
console.log(inputValues)

for (let i=0; i < botones.length; i++){

    botones[i].onclick = function(){
        let confirmacion = window.confirm('Deseas eliminar este producto?');

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
    console.log(input.name)

}
