# Sesión #3: Pipeline en Airflow

## Objetivos

Con todo lo que hemos aprendido hasta el momento serás capaz de crear un DAG por ti mismo para interactuar con servicios externos de AWS.

- Crear conexiones a servicios de AWS
- Realizar operaciones básicas con un almacén de datos como Redshift
  - Exportar datos
  - Cargar datos
  - Crear objetos

## Requisitos

- Acceso al servicio de Amazon Redshift
  - Lectura
  - Escritura
- Acceso a un servicio de S3 en la misma región que Amazon Redshift
  - Lectura
  - Escritura
- (Opcional) [Base de datos de ejemplo](https://docs.aws.amazon.com/redshift/latest/dg/c_sampledb.html)

## Desarrollo

Selecciona alguno de los procesos semiautomáticos que realizan en tu equipo de trabajo y automatizalo con Airflow de manera parcial o total.

> Puedes usar tu base de datos de desarrollo o usar una de las bases de datos de ejemplo que ofrece Amazon Redshift.

1. Crear un diseño de las tareas necesarias para completar el proceso
2. Selecciona el subconjunto de tareas que pueden ser completadas con el conocimiento adquirido hasta el momento.
3. Redefine el proceso enfocandote solo en este último conjunto de tareas
4. Dibuja el grafo que representará el flujo de trabajo
5. Crea y prueba las conexiones necesarias
6. Implementa tu solución en un archivo DAG

> **Nota**: Sientete libre de utilizar cualquier otro operador que necesites para completar esta tarea.
