# Ejemplo #2 - Pruebas de calidad a nivel columna

## Objetivo

- Realizar pruebas de calidad a nivel columna:
    - valores únicos
    - valores distintos
    - valores nulos
    - valor mínimo
    - valor máximo

## Desarrollo

Crearemos un conjunto de pruebas para la tabla `film`, de la base de datos `dvdrental`, usando las siguientes columnas: `rating`, `title` y `rental_duration`.

Para ello utilizaremos el operador [SQLColumnCheckOperator](https://pypi.org/project/apache-airflow-providers-common-sql/).

Antes de escribir la primera línea de código, vamos a crear una nueva conexión, de tipo `Postgres`, utilizando la interfaz web de Airflow.

1. Ir a `Admin > Connections`
2. Hacer click en el botón [+] para agregar una nueva conexión
3. Seleccionamos `Postgres` como tipo de conexión y utilizamos los parámetros que se muestran en la siguiente imagen para completar los campos. *Recuerda que las credenciales son airflow/airflow para el usuario/password*.

![image](/Sesion-05/Ejemplo-02/assets/img/postgres_connection.png)

> No olvides guardar la conexión cuando acbaes de configurarla.

Para vericar que contamos con el proveedor Cmmon SQL Provider instalado en nuestro ambiente, usamos la interfaz web de Airflow: `Admin > Providers`

![image](/Sesion-05/Ejemplo-02/assets/img/commonSQLprovider.png)

Ahora es tiempo de crear nuestro archivo DAG.

1. Importamos la clase

    ```python
    from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator
    ```

2. Creamos una tarea `SQLColumnCheckOperator` y configuramos las reglas de prueba. La definición de estas pruebas se hace mediante un diccionario, en donde:

    - la llave corresponden al nombre de la columna de la tabla
    - el valor es otro diccionario que continene las reglas que se deben cumplir. Este diccionario tiene la siguiente estructura:
        - la llave es nombre de la prueba, por ejemplo, `unique_check`, `null_check`, etc.
        - el valor es un diccionario con parámetros relacionados al tipo de prueba, indistintamente incluye un clasificador: `less_than`, `leq_to`, `greater_than`, `geq_to`, `equal_to`, que hace referencia a un operador de comparación: `<`, `<=`, `>`, `>=`, `=`.

    ```python
    {
        "rating": {"unique_check": {"equal_to": 0}},
        "title": {
            "distinct_check": {"geq_to": 10},
            "null_check": {"equal_to": 0}},
        "rental_duration": {
            "min": {"less_than": 2},
            "max": {"equal_to": 100, "tolerance": 0.1}}
    }
    ```
3. Pasamos este diccionario al parámetro `column_mapping` del operador `SQLColumnCheckOperator`.

4. Especificamos el nombre de la tabla a travvés del parámetro `table`.

5. Establecemos el id de conexión `postgres` a la base de datos por medio del parámetro `conn_id`

6. Ejecutamos el DAG y revisamos la salida del log

El siguiente es un extracto de los resultados de la tarea.
```bash
Record: [('rating', 'unique_check', 995),
         ('title', 'distinct_check', 1000),
         ('title', 'null_check', 0),
         ('rental_duration', 'min', 3),
         ('rental_duration', 'max', 7)]
```

La siguiente tabla resume las reglas, las consultas generadoas, los resultados de la consulta y el resultado final de cada prueba.

|columna| regla | valor esperado | SQL| Descripción | Resultado | Success|
|-|-|-|-|-|-|-|
 |rating|valores únicos| = 0 | `SELECT  COUNT(rating) - COUNT(DISTINCT(rating)) AS rating_unique_check FROM film` | La diferencia entre el total de valores de la columna `rating` y el número de valores distintos de la misma columna debe ser `0`| `995`| `False` |
|title|valores distintos| >= 10| `SELECT COUNT(DISTINCT(title)) AS title_distinct_check FROM film` | El número de valores distintos de `title` debe ser mayor o igual a `10`| `1000`| `True`|
|title|valores nulos | = 0 | `SELECT SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) AS title_null_check FROM film `|El total de valores nulos en el campo `title` debe ser `0`|`0`|`True`|
|rental_duration| valor mínimo | < 2 | `SELECT MIN(rental_duration) AS rental_duration_min FROM film`|El valor mínimo de `rental_duration` debe ser menor a `2`| `3`|`False`|
|rental_duration| valor máximo | =100 ±10| `SELECT MAX(rental_duration) AS rental_duration_max FROM film` |El máximo valor de `rental_duration` debe estar entre `90` y `110`|`7`|`False`|

El resultado global de la prueba esta condicionado a que todas sus pruebas sean exitosas. En otras palabras, para que la tarea sea marcada como exitosa todos los resultados deben ser positivos

El archivo DAG
[s05e05_quality_check_fail.py](/Sesion-05/Ejemplo-02/assets/dags/s05e05_quality_check_fail.py) contine la definición del ejemplo completo.
