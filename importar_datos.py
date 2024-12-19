<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consultas a la Base de Datos</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>

<div class="container mt-5">
    <h2>Consulta de Información</h2>
    <form id="consultaForm">
        <div class="form-group">
            <label for="consultaType">Selecciona una consulta:</label>
            <select class="form-control" id="consultaType">
                <option value="/consulta/docentes">Cantidad de Cursos por Docente</option>
                <option value="/consulta/aulas">Nivel de Ocupación Aula 103</option>
                <option value="/consulta/cursos/computacion_grafica">Días y Turno de Computación Gráfica</option>
                <option value="/consulta/ocupacion_docentes_tarde">Ocupación Docentes en el Turno Tarde</option>
                <option value="/consulta/cursos/matematicas_discretas">Días y Turno de Matemáticas Discretas</option>
                <option value="/consulta/cursos/mañana">Cursos de la Mañana</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Consultar</button>
    </form>

    <h3 class="mt-4">Resultados:</h3>
    <pre id="resultados"></pre>
</div>

<script>
    $(document).ready(function() {
        $("#consultaForm").submit(function(event) {
            event.preventDefault();

            const consultaSeleccionada = $("#consultaType").val();

            // Hacer la solicitud GET a la API de Flask en la URL correcta
            $.get("http://localhost:5000" + consultaSeleccionada, function(data) {
                $("#resultados").text(JSON.stringify(data, null, 2)); // Mostrar los resultados de forma bonita
            }).fail(function() {
                $("#resultados").text("Ocurrió un error al realizar la consulta.");
            });
        });
    });
</script>

</body>
</html>
