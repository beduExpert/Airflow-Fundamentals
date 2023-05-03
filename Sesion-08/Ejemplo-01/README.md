# Ejemplo #1 - Variables de Entorno

## Objetivo

* Utilizar la capa de variables de entorno para almacenar y recuperar variables genéricas
* Almacenar y utilizar conexiones des una variable de entorno

## Desarrollo

En este ejemplo utilizaremos la capa de variables de entorno para almacenar una variable y una conexión.

Recuerda que para que Airflow reconozca el tipo de variable que estas almacenando debes seguir la siguiente convención:

- `AIRFLOW_VAR_{VARIABLE_NAME}`. Variable genérica
- `AIRFLOW_CONN_{CONN_ID}`. Connexión en formato URI con codificación URL.

### Parte I. Variables Genéricos

1. Abrir el archivo docker'compose.yaml
2. Ir a la sección `&airflow-common-env`

    ```YAML
    version: '3'
    x-airflow-common:
    &airflow-common  
    image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.5.1}
    environment:
        &airflow-common-env
        AIRFLOW_VAR_MI_VARIABLE: 6
    ```

3. Agregar la variable `MI_VARIABLE` usando como prefijo `AIRFLOW__VAR__`
4. Reiniciar todos los servicios de docker

    ```bash
    docker-compose stop && docker-compose up
    ```

5. Escribir un DAG para mostrar el contenido de la variable

    ```python
    from airflow.models import Variable
    ...
    def muestra_env_var():
        @task
        def display():
            mi_variable = Variable.get('MI_VARIABLE',None)
            print(mi_variable)
        display()
    muestra_env_var()
    ```

6. Después de guardar el DAG, lo activamos y ejecutamos
7. Abrimos el log de la tarea `display` para comprobar que el valor `6` aparezca

### Parte II. Conexiones

Vamos a agregar una conexión usando la capa de variables de entorno.

1. Abrir el archivo `docker-compose.yaml`
2. Agregar una conexión HTTP

    ```yaml
    AIRFLOW_CONN_HTTP_ENV_VAR: http://https%3A%2F%2Fapi.nasa.gov%2Fplanetary
    ```

3. Reiniciar los contenedores

    ```bash
    docker-compose stop && docker-compose up
    ```

4. Crear un DAG para comprobar y usar la conexión

    ```python
    extrae_datos = SimpleHttpOperator(
        task_id='extrae_metadatos',
        http_conn_id='HTTP_ENV_VAR',
        endpoint='/apod?api_key=DEMO_KEY',        
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )
    ```

5. Guardar, activar y ejecutar el DAG
6. Abrir el log de la tarea `extrae_datos` y comprobar que la solicitud HTTP ha sido exitosa

En las siguientes ligas encontrarás los DAGs para realizar las pruebas

- [**`muestra_env_var.py`**](/Sesion-08/Ejemplo-01/assets/dags/muestra_env_var.py)
- [**`prueba_conexion.py`**](/Sesion-08/Ejemplo-01/assets/dags/prueba_conexion.py)
