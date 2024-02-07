function perfilForm(){
    let form = document.getElementById('perfil-form');
    let botonForm = document.getElementById('perfil-form-boton')

    botonForm.onclick = function(){
        form.submit();
    }
}

perfilForm();