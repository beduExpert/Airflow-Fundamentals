# Cómo ejecutar Airflow usando Docker

Utilizaremos la última imagen de Docker oficial disponible en el [repositorio](https://hub.docker.com/r/apache/airflow) de Airflow.

Si no cuentas con Docker puedes seguir cualquiera de las siguientes guías de instalación:

- [osx](os.md)
- [ubuntu](ubuntu.md)
- [windows](windows.md)

1. Abrir una terminal
2. Creamos una carpeta `mkdir airflow && cd airflow` y nos cambiamos a esa ubicación para convertirlo en nuestro directorio de trabajo.
3. Descargamos el archivo YAML con la definición de todos los servicios de Airflow

    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml'
    ```

4. Crear las siguientes carpetas `dags`, `logs` y `plugins`.

    ```bash
    mkdir -p ./dags ./logs ./plugins
    ```

5. (Solo Linux) Crear un archivo `.env` que contenga la variable de ambiente  `AIRFLOW_UID`

    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

6. Inicializar la base de datos

    ```bash
    docker compose up airflow-init
    ```

7. Ejectuar airflow

    ```bash
    docker compose up
    ```

8. En una segunda terminal ejecuta `docker ps` para verificar que los seis contenedores tengan el estado `(healthy)`

    ```bash
    CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                                       NAMES
    ad53fd953198   apache/airflow:2.5.1   "/usr/bin/dumb-init …"   17 minutes ago   Up 17 minutes (healthy)   8080/tcp                                    airflow-airflow-worker-1
    6475baada6c1   apache/airflow:2.5.1   "/usr/bin/dumb-init …"   17 minutes ago   Up 17 minutes (healthy)   8080/tcp                                    airflow-airflow-scheduler-1
    27c8b514668e   apache/airflow:2.5.1   "/usr/bin/dumb-init …"   17 minutes ago   Up 17 minutes (healthy)   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   airflow-airflow-webserver-1
    65fb3a1b0725   apache/airflow:2.5.1   "/usr/bin/dumb-init …"   17 minutes ago   Up 17 minutes (healthy)   8080/tcp                                    airflow-airflow-triggerer-1
    234e2ca33d24   postgres:13            "docker-entrypoint.s…"   20 minutes ago   Up 20 minutes (healthy)   5432/tcp                                    airflow-postgres-1
    cf1a9c674a2d   redis:latest           "docker-entrypoint.s…"   20 minutes ago   Up 20 minutes (healthy)   6379/tcp                                    airflow-redis-1
    ```

9. Abrir un navegador web usando la siguiente dirección [http://localhost:8080](http://localhost:8080)

10. Usar `airflow` como usuario y password en la página de login

![image](img/airflow_login.png)


## Preparar el ambiente de desarrollo

1. Instalar [Visual Studio Code](https://code.visualstudio.com/download) (VS Code)
2. Instalar [paquete de extension para Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. Instalar [paquete de extension para Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. Instalar modulo de airflow, de preferencia en una ambiente virtual con Python 3.10

    ```bash
    pip install "apache-airflow[celery]==2.5.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.7.txt"
    ```

## Recursos

- [Guía oficial](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) de la installación de la versión 2.5.1
