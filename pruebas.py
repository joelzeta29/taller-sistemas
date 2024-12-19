from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
# consultas a nivel gerencial #
#--------------------------------------------------------------------------------------------

# Ruta1: Consulta de cantidad de cursos por docente:
@app.route('/consulta/docentes', methods=['GET'])
def consulta_docentes():
    return ejecutar_consulta('''
        SELECT nombre_docente, COUNT(DISTINCT codigo_curso) AS cantidad_de_cursos
        FROM horario
        GROUP BY nombre_docente;
    ''')
#RUTA EN MYSQL
                #SELECT nombre_docente, COUNT(DISTINCT codigo_curso) AS cantidad_de_cursos
                #FROM horario
                #GROUP BY nombre_docente;
#------------------------------------------------------------------------------------------

# Ruta2:  Nivel de ocupación en porcentaje del aula 103 los días lunes
@app.route('/consulta/aulas', methods=['GET'])
def nivel_ocupacion_aula_103_lunes():
    return ejecutar_consulta('''
        SELECT
            (COUNT(DISTINCT lunes) / 12) * 100 AS porcentaje_ocupacion
        FROM horario
        WHERE salon = '103' AND lunes IS NOT NULL;
    ''')
        #SELECT
        #    (COUNT(DISTINCT lunes) / 12) * 100 AS porcentaje_ocupacion
        #FROM horario
        #WHERE salon = '103' AND lunes IS NOT NULL;


#ruta: Consulta para obtener los días, salón y turno del curso "Computación Gráfica":
@app.route('/consulta/cursos/computacion_grafica', methods=['GET'])
def consulta_computacion_grafica():
    return ejecutar_consulta('''
        SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        FROM horario
        WHERE nombre_curso = 'Computación Gráfica';
    ''')
        #SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        #FROM horario
        #WHERE nombre_curso = 'Computación Gráfica';

#ruta4: Nivel de ocupación de cada docente en el turno tarde de lunes a viernes
@app.route('/consulta/ocupacion_docentes_tarde', methods=['GET'])
def consulta_ocupacion_docentes_tarde():
    return ejecutar_consulta('''
        SELECT nombre_docente,
               (COUNT(DISTINCT CASE WHEN lunes IS NOT NULL THEN lunes END) / 6) * 100 AS ocupacion_lunes,
               (COUNT(DISTINCT CASE WHEN martes IS NOT NULL THEN martes END) / 6) * 100 AS ocupacion_martes,
               (COUNT(DISTINCT CASE WHEN miercoles IS NOT NULL THEN miercoles END) / 6) * 100 AS ocupacion_miercoles,
               (COUNT(DISTINCT CASE WHEN jueves IS NOT NULL THEN jueves END) / 6) * 100 AS ocupacion_jueves,
               (COUNT(DISTINCT CASE WHEN viernes IS NOT NULL THEN viernes END) / 6) * 100 AS ocupacion_viernes
        FROM horario
        WHERE turno = 'Tarde'
        GROUP BY nombre_docente;
    ''')
            #SELECT nombre_docente,
            #       (COUNT(DISTINCT CASE WHEN lunes IS NOT NULL THEN lunes END) / 6) * 100 AS ocupacion_lunes,
            #       (COUNT(DISTINCT CASE WHEN martes IS NOT NULL THEN martes END) / 6) * 100 AS ocupacion_martes,
            #       (COUNT(DISTINCT CASE WHEN miercoles IS NOT NULL THEN miercoles END) / 6) * 100 AS ocupacion_miercoles,
            #       (COUNT(DISTINCT CASE WHEN jueves IS NOT NULL THEN jueves END) / 6) * 100 AS ocupacion_jueves,
            #       (COUNT(DISTINCT CASE WHEN viernes IS NOT NULL THEN viernes END) / 6) * 100 AS ocupacion_viernes
            #FROM horario
            #WHERE turno = 'T'
            #GROUP BY nombre_docente;
# Función genérica para ejecutar consultas SQL

#ruta 5: ¿Cuáles son los días y el turno en los que se imparte el curso "Matemáticas Discretas"?
@app.route('/consulta/cursos/matematicas_discretas', methods=['GET'])
def consulta_matematicas_discretas():
    return ejecutar_consulta(''' 
        SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        FROM horario
        WHERE nombre_curso = 'Matemáticas Discretas';
    ''')
        #SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        #FROM horario
        #WHERE nombre_curso = 'Matemáticas Discretas';
#RUTA 6: ¿Cuáles son los cursos que se imparten en la mañana?
@app.route('/consulta/cursos/mañana', methods=['GET'])
def consulta_cursos_manana():
    return ejecutar_consulta(''' 
        SELECT nombre_curso, lunes, martes, miercoles, jueves, viernes, salon
        FROM horario
        WHERE turno = 'M';
    ''')
            #SELECT nombre_curso, lunes, martes, miercoles, jueves, viernes, salon
            #FROM horario
            #WHERE turno = 'M';
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
