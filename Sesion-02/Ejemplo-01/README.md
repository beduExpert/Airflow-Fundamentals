# Ejemplo 01 - Fotografía astronómica del día (APOD por sus siglas en inglés)

## Objetivo

* Crear una tarea que obtenga metadatos de fuentes externas usando un comanndo BASH
* Crear una tarea que descargué la fotografía del día usando una función de Python
* Crear una tarea que contabilice el número de fotografías descargadas

## Desarrollo

1. Abrir VS Code
2. Abrir la carpeta `airflow` que creamos en el ejemplo anterior
3. Copiar el archivo [`Sesion-02/Ejemplo-01/assets/dags/apod.py`](assets/dags/apod.py) al directorio de trabajo dentro de la carpeta `dags`.
4. Ir a la interfaz de Airflow [localhost:8080](localhost:8080)
5. Seleccionar el dag `ejemplo1_apod` de la lista
6. Activar el DAG
7. Disparar el DAG
8. Una vez terminada la ejecución, hacer click en cada una de las tareas y explorar los resultados del log.
9. En VS Code explorar el contenido de la carpeta `dags` y abrir el archivo `apod.json` y el archivo `.jpg`
