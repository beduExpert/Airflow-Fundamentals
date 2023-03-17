# Ejecución de Airflow con contenedores

## Objetivo

- Ejecutar Airflow de manera local
- Preparar el ambiente de desarrollo

Utilizaremos la última imagen de Docker oficial disponible en el [repositorio](https://hub.docker.com/r/apache/airflow) de Airflow.

## Desarrollo

>**💡 Nota para experto(a)**
>
> Para ejecutar Airflow a través de contenedores virtualizaods
> es necesario tener instalado Docker Desktop

### Parte I. Ejecutar Airflow

1. Abrir una terminal
2. Verificar que tenemos instalado Docker Desktop

    ```bash
    docker desktop --version
    ```

3. Crear una carpeta y cambiarse a esa ubicación para convertirla en el directorio de trabajo

    ```bash
    mkdir airflow && cd airflow
    ```

4. Descargar el archivo YAML con la definición de todos los servicios de Airflow:

    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml'
    ```

5. Crear las siguientes carpetas: `dags`, `logs` y `plugins`.

    ```bash
    mkdir -p ./dags ./logs ./plugins
    ```

6. Crear un archivo `.env` que contenga la variable de ambiente `AIRFLOW_UID`

    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

7. Inicializar la base de datos (única ocasión)

    ```bash
    docker compose up airflow-init
    ```

8. Ejecutar airflow y sus componentes

    ```bash
    docker compose up
    ```

9. Abrir una segunda terminal y verificar que todos los contenedores aparezcan con el estado `healty`

    ```bash
    docker ps
    ```

    |NAMES                         |STATUS|
    |-|-|
    |airflow-airflow-triggerer-1   |Up 5 minutes (healthy)|
    |airflow-airflow-webserver-1   |Up 5 minutes (healthy)|
    |airflow-airflow-worker-1      |Up 5 minutes (healthy)|
    |airflow-airflow-scheduler-1   |Up 5 minutes (healthy)|
    |airflow-postgres-1            |Up 5 minutes (healthy)|
    |airflow-redis-1               |Up 5 minutes (healthy)|


    > Si alguno de los contenedores no tiene el estado `healty`, puedes revisar los logs con `docker logs airflow-<nombre-del-contenedor>`.
    > Trata de encontrar el error y corregirlo, reiniciar Airflow con `docker-compose down` y luego `docker-compose up` y espera a que
    > todos los contenedores tengan el estado `healthy`


10. Abrir un navegador web usando la siguiente dirección [http://localhost:8080](http://localhost:8080)
11. Usar airflow como usuario y password en la página de inicio de sesión

![airflow login](assets/img/airflow_login.png)

