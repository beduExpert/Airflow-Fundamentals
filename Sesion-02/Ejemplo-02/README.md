# Ejemplo 02 - Tareas de flujo

En este ejemplo vamos a crear un DAG utilzar la API pública [Weather Forecast API](https://open-meteo.com/en/docs#latitude=19.43&longitude=-99.13&hourly=temperature_2m) para obtener la predicción la temperatura de los siguientes 6 días en la Ciudad de México.

## Objetivo

* Crear una **tarea de flujo**  para consultar la temperatura actual y la de pasado mañana
* Crear una **tarea de flujo** para transformar la temperatura de Celsius a Farenheit

## Desarrollo

1. Abrir VS Code
2. Abrir la carpeta `airflow` que creamos en el ejemplo anterior
3. Copiar el archivo [`Sesion-02/Ejemplo-02/assets/dags/temperatura.py`](assets/dags/apod.py) al directorio de trabajo dentro de la carpeta `dags`.
4. Ir a la interfaz de Airflow [localhost:8080](localhost:8080)
5. Seleccionar el dag `ejemplo2_temperatura` de la lista
6. Activar el DAG
7. Disparar el DAG
8. Una vez terminada la ejecución, hacer click en cada una de las tareas y explorar los resultados del log y los Xcom.
