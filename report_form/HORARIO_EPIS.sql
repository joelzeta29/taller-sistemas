USE TALLER;
CREATE TABLE horario (
    codigo_curso VARCHAR(10),
    area_curricular VARCHAR(50),
    nombre_curso VARCHAR(100),
    grado_semestre VARCHAR(10),
    grupo VARCHAR(10),
    turno VARCHAR(10),
    salon VARCHAR(10),
    nombre_docente VARCHAR(100),
    lunes VARCHAR(20),
    martes VARCHAR(20),
    miercoles VARCHAR(20),
    jueves VARCHAR(20),
    viernes VARCHAR(20)
);
LOAD DATA INFILE 'E:/SEMESTRE 10 - 2/TALLER DE IMPEMENTACION/TALLER DE SISTEMAS/horario_limpio.csv'
INTO TABLE horario
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

DESCRIBE horario;
ALTER TABLE horario 
MODIFY COLUMN codigo_curso VARCHAR(20), 
MODIFY COLUMN area_curricular VARCHAR(100), 
MODIFY COLUMN nombre_curso VARCHAR(200), 
MODIFY COLUMN grado_semestre VARCHAR(20),
MODIFY COLUMN grupo VARCHAR(20),
MODIFY COLUMN turno VARCHAR(20),
MODIFY COLUMN salon VARCHAR(20),
MODIFY COLUMN nombre_docente VARCHAR(150),
MODIFY COLUMN lunes VARCHAR(50),
MODIFY COLUMN martes VARCHAR(50),
MODIFY COLUMN miercoles VARCHAR(50),
MODIFY COLUMN jueves VARCHAR(50),
MODIFY COLUMN viernes VARCHAR(50);

SELECT lunes, martes, miercoles, jueves, viernes, salon, turno
        FROM horario
        WHERE nombre_curso = 'Matemáticas Discretas'






