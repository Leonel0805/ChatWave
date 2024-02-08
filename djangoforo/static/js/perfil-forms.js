function SubmitForm(formId, buttonId) {
    let form = document.getElementById(formId);
    let botonForm = document.getElementById(buttonId);
    
    if (form && botonForm) {
        botonForm.onclick = function() {
            form.submit();
        }
    } else {
        console.error(`Los elementos HTML de ${formId} no están presentes en la página.`);
    }
}

console.log('holaaaaaa')

SubmitForm('perfil-form', 'perfil-form-boton')
SubmitForm('room-form', 'room-form-boton')

