# Reto #3 - Calendario laboral sin dias feriados

## Objetivo

* Crear un plan de ejecución personalizado

## Desarrollo

1. Crear un plugin de tipo timetable
2. Registrar el plugin
3. Crear un DAG de ejemplo con un operador `EmptyOperator` que utilice la nueva tabla de tiempo
4. Usar el parámetro `catchup` para ejecutar el DAG desde de el comienzo del año hasta la fecha actual.

Tip: Utilizar el código fuente de Airflow [workday](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/example_dags/plugins/workday.html)
