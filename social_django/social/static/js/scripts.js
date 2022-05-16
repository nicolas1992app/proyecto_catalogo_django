"use strict";

let URLDomain = document.location.origin+"/";
let idBorrar = 0;
let rutaBorrado = $('#rutaBorrado').val();
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

/*Logica para recibir modal de crear y editar*/
function abrirModalCrearCatalogo(url) {
    cargarAbrirModal($("#_crearEditar"), url,function () {
        const form = $("#catalogForm")[0];
        agregarValidacionForm(form, function (event) {
            enviarFormularioAsync(form, url).then(exitoso => {
                if (exitoso)
                    location.reload();
            });
            return true;
        });
    });
}

function abrirModalCrearUsuarios(url) {
    cargarAbrirModal($("#_crearEditarUsuarios"), url,function () {
        const form = $("#registoUsuarioForm")[0];
        agregarValidacionForm(form, function (event) {
            enviarFormularioAsync(form, url).then(exitoso => {
                if (exitoso)
                    location.reload();
            });
            return true;
        });
    });
}

function agregarValidacionForm(form, fnCallback){
    form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
        } else {
            if(fnCallback !== undefined)
                if(fnCallback(event)) {
                    event.preventDefault();
                    event.stopPropagation();
                }
        }
    }, false);
}

function cargarAbrirModal(modal, url, fnCallback) {
	if(typeof modal === 'string') {
		modal = $(`#${modal}`);
	}

	$.get(url).then(responseText => {
		try {
			if (responseText.includes("<!DOCTYPE html>")) {
				console.log('No tiene permisos para acceder a esta funcionalidad');
				return false;
			}
			modal.html(responseText);
			modal.modal('show');

			if((fnCallback !== undefined) && (typeof(fnCallback) === 'function'))
				fnCallback(url);

		} catch (err) {
			console.log(err);
		}
	}).catch(error => {
		console.log(error);
	});

	return modal;
}

async function enviarFormularioAsync(form, url, mensaje='') {
    if(typeof form === 'string') {
        form = $(`#${form}`)[0];
    }

    const  formData = new FormData(form);

    try {
        const datos = JSON.parse(await $.ajax({
            url: url,
            type: "post",
            dataType: "html",
            data: formData,
            cache: false,
            processData: false,
            contentType: false
        }));

        if (datos.estado === 'OK') {
            if(datos.mensaje)
                console.log(datos.mensaje);
            return true;
        } else {
            console.log(datos.estado === 'error' ? datos.mensaje : 'No tiene permisos para acceder a esta funcionalidad');
            return false;
        }
    } catch (e) {
        console.error(e);
        return false;
    } finally {
    }
}

function fConfirmarEliminar(idElemento, justificar, fnCallback) {
    if (justificar){
        fSweetAlertEliminarJustificado(fnCallback);
    }else{
        fSweetAlert(fnCallback);
    }

    idBorrar = idElemento;
}

function fSweetAlert(fnCallback) {
    Swal.fire({
        title: '¿Está seguro de eliminar este item?',
        text: "Esta acción no se podrá revertir",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '¡Sí, eliminarlo!',
        cancelButtonText: 'Cancelar'
    }).then(result => {
        confirmarEliminacion(result.value, URLDomain + rutaBorrado + "/" + idBorrar + "/delete", fnCallback)
    });
}

function fSweetAlertEliminarJustificado(fnCallback) {
    Swal.fire({
        title: '¿Está seguro de eliminar este item?',
        text: "Esta acción no se podrá revertir",
        icon: 'warning',
        input: 'text',
        inputPlaceholder: '¿Por qué deseas eliminar este item?',
        inputValue: '',
        inputAttributes: {'maxlength': 100},
        showCancelButton: true,
        confirmButtonText: '¡Sí, eliminarlo!',
        cancelButtonText: 'Cancelar',
        inputValidator: (value) => {
            if (!value) {
              return '¡Debes justificar esta acción!'
            }
        }
    }).then(result => {
        confirmarEliminacion(result.value, URLDomain + rutaBorrado + "/" + idBorrar + "/delete", fnCallback)
    });
}


function confirmarEliminacion(valor, url, fnCallback) {
    if (valor) {
        $.ajax({
            url: url,
            type: 'POST',
            context: document.body,
            data:JSON.stringify({'justificacion': valor}),
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                if(data.estado === "OK") {
                    if((fnCallback !== undefined) && (typeof(fnCallback) === 'function'))
                    {
                        fnCallback();
                    }else{
                        location.reload();
                    }
                }else if(data.estado === "error"){
                    console.log(data.mensaje);
                }
                else {
                    console.log('No tiene permisos para acceder a esta funcionalidad');
                }
            },
            failure: function (errMsg) {
                if((fnCallback !== undefined) && (typeof(fnCallback) === 'function'))
                    {
                        fnCallback();
                    }else{
                        location.reload();
                    }
            }
        });
    }
}

