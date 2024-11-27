// Variables globales para almacenar datos originales
let datosAutores = [];
let datosLibros = [];

function cargarConPaginacion(data, tablaId, filasPorPagina = 5) {
    const tabla = document.getElementById(tablaId);
    const totalFilas = data.length;
    let paginaActual = 1;
    const totalPaginas = Math.ceil(totalFilas / filasPorPagina);

    // Función para renderizar una página específica
    function renderizarPagina(pagina) {
        tabla.innerHTML = ''; // Limpia la tabla
        const inicio = (pagina - 1) * filasPorPagina;
        const fin = inicio + filasPorPagina;

        data.slice(inicio, fin).forEach(fila => {
            tabla.insertAdjacentHTML('beforeend', fila); // Agrega las filas correspondientes
        });

        document.getElementById(`${tablaId}-paginacion`).innerText = `Página ${pagina} de ${totalPaginas}`;
    }

    // Navegación entre páginas
    document.getElementById(`${tablaId}-prev`).addEventListener('click', () => {
        if (paginaActual > 1) {
            paginaActual--;
            renderizarPagina(paginaActual);
        }
    });

    document.getElementById(`${tablaId}-next`).addEventListener('click', () => {
        if (paginaActual < totalPaginas) {
            paginaActual++;
            renderizarPagina(paginaActual);
        }
    });

    // Renderiza la primera página al cargar
    renderizarPagina(paginaActual);
}

// Para usar la paginación
function cargarAutores() {
    $.getJSON('/obtener-autores/', function(data) {
        datosAutores = data.data.map(autor => `
            <tr>
                <td>${autor.nombre}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editarAutor(${autor.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="eliminarAutor(${autor.id})">Eliminar</button>
                </td>
            </tr>
        `);
        cargarConPaginacion(datosAutores, 'tabla-autores');
        cargarAutoresSelect();
    });
}

// Para usar la paginación
function cargarLibros() {
    $.getJSON('/obtener-libros/', function(data) {
        datosLibros = data.data.map(libro => `
            <tr>
                <td>${libro.titulo}</td>
                <td>${libro.autor}</td>
                <td>${libro.editorial}</td>
                <td>${libro.anio}</td>
                <td>${libro.isbn}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editarLibro(${libro.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="eliminarLibro(${libro.id})">Eliminar</button>
                </td>
            </tr>
        `);
        cargarConPaginacion(datosLibros, 'tabla-libros');
    });
}

//  Función para llenar el menú desplegable de autores en el modal de agregar libro
function cargarAutoresSelect() {
    $.getJSON('/obtener-autores/', function(data) {
        let opciones = '';
        data.data.forEach(autor => {
            opciones += `<option value="${autor.id}">${autor.nombre}</option>`;
        });
        $('#autor-libro').html(opciones);
        $('#editar-autor-libro').html(opciones);
    });
}

// Función para agregar un nuevo autor
function agregarAutor() {
    const nombre = $('#nombre-autor').val();
    $.post('/agregar-autor/', {nombre: nombre, csrfmiddlewaretoken: '{{ csrf_token }}'}, function(data) {
        if (data.status === 'ok') {
            $('#modal-agregar-autor').modal('hide');
            $('#nombre-autor').val(''); // Limpiar el campo
            cargarAutores();
        }
    });
}

// Función para agregar un nuevo libro
function agregarLibro() {
    const titulo = $('#titulo-libro').val();
    const autorId = $('#autor-libro').val();
    const editorial = $('#editorial-libro').val();
    const anio = $('#anio-libro').val();
    const isbn = $('#isbn-libro').val();
    $.post('/agregar-libro/', {
        titulo: titulo,
        autor: autorId,
        editorial: editorial,
        anio: anio,
        isbn: isbn,
        csrfmiddlewaretoken: '{{ csrf_token }}'
    }, function(data) {
        if (data.status === 'ok') {
            $('#modal-agregar-libro').modal('hide');
            $('#titulo-libro').val(''); // Limpiar el campo de título
            $('#autor-libro').val(''); // Limpiar el campo de autor
            $('#editorial-libro').val(''); // Limpiar el campo de editorial
            $('#anio-libro').val(''); // Limpiar el campo de anio
            $('#isbn-libro').val(''); // Limpiar el campo de isbn
            cargarLibros();
        }
    });
}

// Función para eliminar un autor
function eliminarAutor(id) {
    $.ajax({
        url: `/eliminar-autor/${id}/`,
        type: 'DELETE',
        headers: {'X-CSRFToken': '{{ csrf_token }}'},
        success: function(data) {
            if (data.status === 'ok') {
                cargarAutores();
                cargarLibros();
            }
        }
    });
}

// Función para eliminar un libro
function eliminarLibro(id) {
    $.ajax({
        url: `/eliminar-libro/${id}/`,
        type: 'DELETE',
        headers: {'X-CSRFToken': '{{ csrf_token }}'},
        success: function(data) {
            if (data.status === 'ok') {
                cargarLibros();
            }
        }
    });
}

// Función para filtrar las tablas por columnas específicas
// Filtrar y actualizar la tabla con los resultados
function filtrarTabla(inputId, datosOriginales, tablaId) {
const filtro = document.getElementById(inputId).value.toLowerCase();
const datosFiltrados = datosOriginales.filter(html => html.toLowerCase().includes(filtro));
cargarConPaginacion(datosFiltrados, tablaId);
}

// Función para editar autor
function editarAutor(id) {
    $.getJSON(`/obtener-autor/${id}/`, function(data) {
        $('#id-autor').val(data.id);
        $('#editar-nombre-autor').val(data.nombre);
        $('#modal-editar-autor').modal('show');
    });
}

// Función para editar libro
function editarLibro(id) {
    $.getJSON(`/obtener-libro/${id}/`, function(data) {
        $('#id-libro').val(data.id);
        $('#editar-titulo-libro').val(data.titulo);
        $('#editar-editorial').val(data.editorial);
        $('#editar-anio').val(data.anio);
        $('#editar-isbn').val(data.isbn);
        cargarAutoresSelect(); // Rellenar el select con autores actualizados
        $('#editar-autor-libro').val(data.autor.id); // Seleccionar el autor actual
        $('#modal-editar-libro').modal('show');
    });
}

// Función para guardar los cambios de autor
function guardarCambiosAutor() {
    const id = $('#id-autor').val();
    const nombre = $('#editar-nombre-autor').val();
    $.post(`/editar-autor/${id}/`, { nombre: nombre, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
        if (data.status === 'ok') {
            $('#modal-editar-autor').modal('hide');
            cargarAutores();
            cargarLibros();
        }
    });
}

// Función para guardar los cambios de libro
function guardarCambiosLibro() {
    const id = $('#id-libro').val();
    const titulo = $('#editar-titulo-libro').val();
    const autorId = $('#editar-autor-libro').val();
    const editorial = $('#editar-editorial').val();
    const anio = $('#editar-anio').val();
    const isbn = $('#editar-isbn').val();
    $.post(`/editar-libro/${id}/`, {
        titulo: titulo,
        autor: autorId,
        editorial: editorial,
        anio: anio,
        isbn: isbn,
        csrfmiddlewaretoken: '{{ csrf_token }}'
    }, function(data) {
        if (data.status === 'ok') {
            $('#modal-editar-libro').modal('hide');
            cargarLibros();;
        }
    });
}

//Eventos de búsqueda
document.getElementById('buscar-autor').addEventListener('input', () => filtrarTabla('buscar-autor', datosAutores, 'tabla-autores'));
document.getElementById('buscar-libro').addEventListener('input', () => filtrarTabla('buscar-libro', datosLibros, 'tabla-libros'));

$(document).ready(function() {
    cargarAutores();
    cargarLibros();
    $('#btn-agregar-autor').click(function() {
        $('#modal-agregar-autor').modal('show');
    });
    $('#btn-agregar-libro').click(function() {
        $('#modal-agregar-libro').modal('show');
    });
    $('#guardar-autor').click(agregarAutor);
    $('#guardar-libro').click(agregarLibro);
});