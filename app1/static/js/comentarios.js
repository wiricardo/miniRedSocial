function cargarPub(idPub)
{
    fetch(`/devolverPublicacion/?idPub=${idPub}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.getElementById('tituloPub').innerHTML = data.titulo
        document.getElementById('autorPub').innerHTML = data.autor
        document.getElementById('descripcionPub').innerHTML = data.descripcion
        document.getElementById('idPublicacion').value = idPub
        imgDiv = document.getElementById('imagenPub')
        imgDiv.innerHTML = ''
        imgDiv.innerHTML = `<img src="${data.imagen}" class="img-fluid rounded" style="max-height: 300px;">`
        seccionComentarios = document.getElementById('comentariosTotales')
        seccionComentarios.innerHTML = ''

        if (data.datosComentario.length === 0)
        {
            seccionComentarios.innerHTML = `<p class='text-muted text-center'>Aun no hay comentarios</p>`
        }

        for (comenInfo of data.datosComentario)
        {
            /*SE AGREGA ESTA SECCION PARA RESPUESTA A COMENTARIOS*/
            bloqueComentario = `
            <div class='border-bottom mb-3 pb-2' id='bloque-${comenInfo.id}'>
                <strong>${comenInfo.autor}</strong><br>
                <p>${comenInfo.descripcion}</p>
                <button class='btn btn-sm btn-outline-secondary' onclick='mostrarFormularioRespuesta(${comenInfo.id}, ${idPub})'>
                    <i class="fa-solid fa-reply"></i> Responder
                </button>
            </div>
            `;

            // PREGUNTA 3 - AGREGAR LAS RESPUESTAS A LOS COMENTARIOS
            /*AGREGANDO RESPUESTAS DE COMENTARIOS */
            
            // ITERAR EN EL ATRIBUTO comenInfo.respuestas
            // CREAR EL BLOQUE HTML CON LA INFORMACION DE LA RESPUESTA
            // ANEXAR ESE BLOQUE AL OBJETO bloqueComentario


            /* FIN DE RESPUESTAS DE COMENTARIOS */

            seccionComentarios.innerHTML += bloqueComentario

        }
    })
}

function enviarComentario()
{
    comentarioUsuario = document.getElementById('comentarioUsuario')
    idPublicacion = document.getElementById('idPublicacion').value

    if(comentarioUsuario.value.trim() === "")
    {
        alert("Por favor escriba un comentario")
        return;
    }

    datos = {
        'comentario':comentarioUsuario.value,
        'idPublicacion':idPublicacion
    }

    fetch('/publicarComentario/',{
        method: 'POST',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        comentarioUsuario.value = ''
        console.log(data)
        cargarPub(idPublicacion)
    })

}


function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== "")
    {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++)
        {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "="))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/* FUNCIONES PARA CREAR RESPUESTAS A COMENTARIOS - EXAMEN FINAL */
function mostrarFormularioRespuesta(idComentario, idPublicacion) {

    // CAPTURA EL CONTENEDOR EN DONDE SE IMPLEMENTARA EL NUEVO FORMULARIO
    const contenedor = document.getElementById(`bloque-${idComentario}`);

    // SI YA EXISTE EL FORMULARIO, SE ELIMINA (TOGGLE)
    const existente = contenedor.querySelector('.form-respuesta');
    if (existente) {
        existente.remove();
        return;
    }

    // PREGUNTA 1 - CREAR EL FORMULARIO CON EL ESPACIO DE TEXTO Y EL BOTON PARA PODER ENVIAR LA RESPUESTA HACIA EL BACKEND
    // TENER EN CUENTA QUE PARA CAPTURAR EL TEXTO DEL COMENTARIO EL ESPACIO DE TEXTO CREADO DEBE TENER UN ID: "respuesta-${idComentario}"
    // EL BOTON A IMPLEMENTAR DEBE TENER ANEXADO COMO EVENTO ONCLICK LA FUNCION enviarRespuesta(<id del comentario>,<id de la publicacion>)
    const formHTML = `
    `;

    // SE INSERTA EL FORMULARIO CREADO POR EL USUARIO
    contenedor.insertAdjacentHTML('beforeend', formHTML);
}


function enviarRespuesta(idComentario, idPublicacion) {
    // PREGUNTA 1 - FUNCION ENVIAR RESPUESTA HACIA EL BACKEND

    // CAPTURAR EL OBJETO DEL FORMULARIO CREADO PREVIAMENTE EN DONDE SE ESCRIBE LA RESPUESTA AL COMENTARIO

    // VALIDAR QUE EL TEXTO CONTENGA CARACTERES VALIDOS USANDO LA FUNCION .TRIM()
    
    // CREAR EL OBJETO JSON CON LOS DATOS INDICADOS EN EL EXAMEN

    // USAR LA FUNCION FETCH PARA ENVIAR LOS DATOS A LA RUTA '/publicarRespuestaComentario/'

    // AL RECIBIR LA RESPUESTA DEL SERVIDOR LIMPIAR EL AREA DE TEXTO DE RESPUESTA AL COMENTARIO Y LLAMAR A LA FUNCION
    // cargarPub PASANDO COMO PARAMETRO EL ID DE LA PUBLICACION (idPublicacion)

}
