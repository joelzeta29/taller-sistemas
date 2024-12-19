from flask import Flask, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Ruta para servir el formulario HTML
@app.route('/')
def index():
    return render_template('formulario.html')

# Consultas a nivel gerencial #
# Ruta1: Consulta de cantidad de cursos por docente
@app.route('/consulta/docentes', methods=['GET'])
def consulta_docentes():
    return ejecutar_consulta('''SELECT nombre_docente, COUNT(DISTINCT codigo_curso) AS cantidad_de_cursos
                                FROM horario
                                GROUP BY nombre_docente;''')

# Ruta2: Nivel de ocupación en porcentaje del aula 103 los días lunes
@app.route('/consulta/aulas', methods=['GET'])
def nivel_ocupacion_aula_103_lunes():
    return ejecutar_consulta('''SELECT (COUNT(DISTINCT lunes) / 12) * 100 AS porcentaje_ocupacion
                                FROM horario WHERE salon = '103' AND lunes IS NOT NULL;''')

# Ruta3: Consulta de días, salón y turno para Computación Gráfica
@app.route('/consulta/cursos/computacion_grafica', methods=['GET'])
def consulta_computacion_grafica():
    return ejecutar_consulta('''SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
                                FROM horario WHERE nombre_curso = 'Computación Gráfica';''')

# Ruta4: Consulta de ocupación de docentes en el turno tarde
@app.route('/consulta/ocupacion_docentes_tarde', methods=['GET'])
def consulta_ocupacion_docentes_tarde():
    return ejecutar_consulta('''SELECT nombre_docente,
                                       (COUNT(DISTINCT CASE WHEN lunes IS NOT NULL THEN lunes END) / 6) * 100 AS ocupacion_lunes,
                                       (COUNT(DISTINCT CASE WHEN martes IS NOT NULL THEN martes END) / 6) * 100 AS ocupacion_martes,
                                       (COUNT(DISTINCT CASE WHEN miercoles IS NOT NULL THEN miercoles END) / 6) * 100 AS ocupacion_miercoles,
                                       (COUNT(DISTINCT CASE WHEN jueves IS NOT NULL THEN jueves END) / 6) * 100 AS ocupacion_jueves,
                                       (COUNT(DISTINCT CASE WHEN viernes IS NOT NULL THEN viernes END) / 6) * 100 AS ocupacion_viernes
                                FROM horario WHERE turno = 'T'
                                GROUP BY nombre_docente;''')
# Ruta5: Consulta para los días y turno del curso "Matemáticas Discretas"
@app.route('/consulta/cursos/Análisis_y_Diseño_de_Algoritmos', methods=['GET'])
def consulta_analisis_y_diseño_de_algoritmos():
    query = '''
        SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        FROM horario
        WHERE nombre_curso = 'Análisis y Diseño de Algoritmos';
    '''
    
    # Ejecutar la consulta
    return ejecutar_consulta(query)

# Ruta6: Consulta de cursos de la mañana
@app.route('/consulta/cursos/mañana', methods=['GET'])
def consulta_cursos_mañana():
    # Definir la consulta SQL
    query = '''
        SELECT nombre_curso, lunes, martes, miercoles, jueves, viernes, salon
        FROM horario
        WHERE turno = 'm';
    '''
    
    # Ejecutar la consulta
    return ejecutar_consulta(query)

def ejecutar_consulta(consulta_sql):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="taller"
        )
        cursor = conexion.cursor()
        cursor.execute(consulta_sql)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        datos = [dict(zip(columnas, fila)) for fila in resultados]
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

if __name__ == '__main__':
    app.run(debug=True)
