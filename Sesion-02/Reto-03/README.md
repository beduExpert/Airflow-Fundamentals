# Reto 3. Definición de dependencias y ejecución programada

## Objetivo

* Familiarizarse con la definición de dependencias entre tareas
* Uso de la herramienta crontab para definir expresiones cron
* Uso de parámetros del DAG

## Desarrollo

Este reto consiste en dos etapas:

    - Reescribir la dependencia entre tareas y 
    - Definir un programa de ejecuión par el DAG

### Parte I. Reescribir la dependencia entre tareas

Utiliza el archivo dag [basic_apod.py](Ejemplo-01/assets/dags/basic_apod.py)

1. Comenta la línea que define las dependencias
2. Define las dependencias utilizando cualquiera de las siguientes funciones: `chain`, `set_upstream` o `set_downstream`
3. Verifica que la visualización del grafo siga siendo la misma después de tus cambios

### Parte II. Definir un programa de ejecuión par el DAG

Programa el DAG para ejecutarse diariamente a las 7 de la mañana, hora estándar del centro.

1. Utiliza el mismo archivo DAG de la parte I
2. Utiliza [crontab guru](https://crontab.guru/) para definir la expresión cron necesaria para ejecutar el DAG diariamente a las 7am CST.
3. Modifica los parámetros del DAG necesarios
4. En la inerfaz de Airflow, selecciona el nombre del DAG y verifica que el valor de `Next Run`.

## Definición de hecho

1. Un archivo DAG con basado en `basic_apod.py` que utiliza una forma alternativa de definición de dependencias diferente al desplazamiento bit `>>`.
2. Un archivo DAG (puede ser el mismo) programado para ejecutarse diariamente a las 7 de la mañana, hora estándar del centro.
