# Reto #2 - Leer conexión desde AWS Secrets Manager

## Objetivo

* Crear un secreto para almacenar una conexión
* Recuperar el secreto y utilizarlo en un DAG

## Desarrollo

En este reto tendrás que configurar el backend de Airflow para que busque las conexiones en AWS Secrets Manager

1. Configurar backend de Airflow
2. Crear un nuevo secreto en AWS Secrets Manager
3. Crear un DAG de prueba
4. Ejecutar el DAG
5. Actualizar el valor de la conexión
6. Ejecutar nuevamente el DAG

Tip: Puedes usar la conexión HTTP o Postgres con las que ya estas familiarizado.