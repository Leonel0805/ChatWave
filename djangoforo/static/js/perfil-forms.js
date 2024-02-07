// function perfilForm(){
//     let form = document.getElementById('perfil-form');
//     let botonForm = document.getElementById('perfil-form-boton')

//     botonForm.onclick = function(){
//         form.submit();
//     }
// }

function RoomForm(){
    let form = document.getElementById('room-form');
    let botonForm = document.getElementById('room-form-boton')

    console.log(botonForm)
    botonForm.onclick = function(){
        console.log(botonForm)

        form.submit();
    }
}

// perfilForm();
RoomForm();