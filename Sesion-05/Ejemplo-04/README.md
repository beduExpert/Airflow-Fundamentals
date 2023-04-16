# Ejemplo #4 - Sensor

Introduciremos el uso de un sensor de tipo HTTP para revisar que una API se encuentre activa.

## Objetivo

- Utilizar el sensor [HttpSensor](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html#httpsensor) para consultar la disponibilidad de una API
- Combinar tareas TaskFlow con algunos operadores tradicionales:    
    - [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html)
    - [SimpleHttpOperator](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html#simplehttpoperator)

## Desarrollo

Vamos a construir un nuevo DAG que realice las siguientes tareas:

- Crear una tabla en Postgres `dvdrental.public.apod`
- Revisar si la API [Astronomy Picture of the Day](https://api.nasa.gov/) esta activa
- Realizar una petición `HTTP` y descargar los metadatos de la fotografía del día
- Transformar la respuesta `JSON` y almacenarla en un archivo con formato `CSV`
![image](/Sesion-05/Ejemplo-04/assets/img/sensor_basico.png)


### Requisitos

- Crear/Utilizar una conexión tipo Postgres con id `postgres`

    ```json
    "postgres": {
        "conn_type": "postgres",
        "description": "",
        "login": "airflow",
        "password": "airflow",
        "host": "postgres",
        "port": 5432,
        "schema": "dvdrental",
        "extra": ""
        }
    ```

- Crear una conexión de tipo HTTP con id `http_default`

    ```json
    "http_default": {
        "conn_type": "http",
        "description": "",
        "login": "",
        "password": null,
        "host": "https://api.nasa.gov/planetary",
        "port": null,
        "schema": "",
        "extra": ""
    }
    ```

### Paso 1. Creamos la tabla

1. Usaremos el siguiente DDL para definir la estructura de la tabla

    ```sql
    --ddl_apod
    CREATE TABLE IF NOT EXISTS apod (
        copyright text,
        date date,
        explanation text,
        hdurl text,
        media_type text,
        service_version text,
        title text,
        url text
    );
    ```

2. Importamos la clase `PostgresOperator` antes de usarla

    ```python
    from airflow.providers.postgres.operators.postgres import PostgresOperator
    ```

3. Creamos una tarea pasando como parámetros el id de conexión y la sentencia SQL para crear la tabla

    ```python
        create_table = PostgresOperator(
            task_id='create_table',
            postgres_conn_id='postgres',
            sql=ddl_apod
        )
    ```

### Paso 2. Configuramos un sensor HTTP que revisé si la API puede recibir peticiones y usaremos el resultado para decidir si las siguientes tareas se ejecutan o no.

1. Importamos la clase `HttpSensor`

    ```python
    from airflow.providers.http.sensors.http import HttpSensor
    ```

2. Creamos la tarea usando los siguientes parámetros

    ```python
    revisa_disponibilidad_api = HttpSensor(
        task_id='revisa_sensor_http',
        endpoint='/apod',
        http_conn_id='http_default',
        request_params={'api_key':'DEMO_KEY'},
        mode='poke',
        poke_interval=30,
        timeout=120,
        response_check=lambda response: "copyright" in response.text,
        soft_fail=True
    )
    ```

- El sensor usa el modo `poke`
    - Se ejecutará cada 30 segundos
    - y después de un lapso de 2 minutos el sensor dejará de intentarlo
- La tarea será marcada como omitida (skipped) si el tiempo de espera es alcanzado
- El criterio para decidir si la API está activa o no se define en base a su respuesta
    - Si la respuesta contiene la palabra 'copyright' se considerá exitosa.
    - Este es un ejemplo de una consulta existosa
        ```bash
        curl -L https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY
        ```

        ```json
        {
        "copyright": "Tunc Tezel",
        "date": "2023-04-15",
        "explanation": "A composite of images ...",
        "hdurl": "https://apod.nasa.gov/apod/image/2304/Ma2022-3.jpg",
        "media_type": "image",
        "service_version": "v1",
        "title": "When Z is for Mars",
        "url": "https://apod.nasa.gov/apod/image/2304/Ma2022-3_1024.jpg"
        }
        ```

3. Para similar una respuesta negativa, vamos a buscar una cadena que no aparece en la respuesta.

    ![image](/Sesion-05/Ejemplo-04/assets/img/sensor_fallido.png)

    ```python
    ...
    response_check=lambda response: "httpbin" in response.text,
    ```

    El siguiente extracto de log muestra 5 peticiones antes de que la tarea se marcada como omitida (SKIPPED).
    
    ```bash
    [2023-04-15, 15:01:16 CDT] {http.py:122} INFO - Poking: /apod
    [2023-04-15, 15:01:16 CDT] {base.py:73} INFO - Using connection ID 'http_default' for task execution.
    [2023-04-15, 15:01:47 CDT] {http.py:122} INFO - Poking: /apod
    [2023-04-15, 15:01:47 CDT] {base.py:73} INFO - Using connection ID 'http_default' for task execution.
    [2023-04-15, 15:02:18 CDT] {http.py:122} INFO - Poking: /apod
    [2023-04-15, 15:02:18 CDT] {base.py:73} INFO - Using connection ID 'http_default' for task execution.
    [2023-04-15, 15:02:48 CDT] {http.py:122} INFO - Poking: /apod
    [2023-04-15, 15:02:49 CDT] {base.py:73} INFO - Using connection ID 'http_default' for task execution.
    [2023-04-15, 15:03:19 CDT] {http.py:122} INFO - Poking: /apod
    [2023-04-15, 15:03:19 CDT] {base.py:73} INFO - Using connection ID 'http_default' for task execution.
    ```

    ```bash
    [2023-04-15, 15:03:20 CDT] {taskinstance.py:1398} INFO - Sensor has timed out; run duration of 124.52581257299971 seconds exceeds the specified timeout of 120.
    ```

    ```bash
    [2023-04-15, 15:03:20 CDT] {taskinstance.py:1323} INFO - Marking task as SKIPPED. dag_id=sensor_basico, task_id=revisa_sensor_http, execution_date=20230415T200110, start_date=20230415T200115, end_date=20230415T200320
    [2023-04-15, 15:03:20 CDT] {local_task_job.py:208} INFO - Task exited with return code 0
    [2023-04-15, 15:03:20 CDT] {taskinstance.py:2578} INFO - 0 downstream tasks scheduled from follow-on schedule check
    ```


### Paso 3. Hacemos la llamada al API para obtener los metadados

1. Importamos `SimpleHttpOperator`

    ```python
    from airflow.providers.http.operators.http import SimpleHttpOperator
    ```

2. Creamos una solicitud tipo `GET` y convertimos la respuesa en un diccionario de Python

    ```python
    extrae_datos = SimpleHttpOperator(
        task_id='extrae_metadatos',
        http_conn_id='http_default',
        endpoint='/apod?api_key=DEMO_KEY',        
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )
    ```

3. Cmprobamos que la respuesta se envíe al XCom


### Paso 4. Creamos un tarea de Python para guardar los datos

1. Importamos el módulo de `pandas`

    ```python
    import pandas as pd
    ```

2. Creamos una tarea de flujo que reciba como parámetros los datoas

    ```python
    @task()
    def almacena_datos(data):
        ...
    ```
3. Después creamos un dataframe de Pandas a partir del diccionario y lo guardamos en formato `CSV`

    ```python
    df_single_row = pd.json_normalize(data)
    df_single_row.to_csv('/tmp/apod.csv', index=False)
    ```

4. Ahora definimos la relación de dependencia entre las tareas

    ```python
    create_table >> revisa_disponibilidad_api >> extrae_datos >> almacena_datos(extrae_datos.output)
    ```

    > Nota: Es necesario pasar explicitamente la salida de la tarea `extrae_datos` como parámetro a la tarea de fljo `almacena_datos`

5. Ejecutamos el DAG completo

6. Nos conectamos al contenedor del worker y ejectuamos el siguiente comando para verificar que el archivo se creo

    ```bash
    cat /tmp/apod.csv
    ```

El ejemplo completo esta disponible en el archivo DAG [s05e12_sensor_http.py](Sesion-05/Ejemplo-04/assets/dags/s05e12_sensor_http.py)
