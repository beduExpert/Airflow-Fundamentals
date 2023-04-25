# Sesión #: Entornos de producción

## :dart: Objetivos

- Integrar alguno de los mecanismos de notificación a un pipeline previamente creado
    - email
    - slack
- Rediseñar el DAG para usar una fecha lógica como parámetro, de tal manera que soporte cargas históricas a través del comando backfill

> Nota: Se recomienda aplicar estos cambios al pipeline creado en la Sesión #3 - Postwork

## ⚙ Requisitos

+ Configurar servicio de correos o espacio de trabajo en Slack
+ Local Airflow


## Desarrollo

1. Crear conexiones necesarias: Slack o Email
2. Usar funciones de callback para enviar notificaciones por error
3. Agregar un tarea para forzar el error y comprobar que funcionen las alertas
4. Usar la función de tipo callback para mandar un mensaje exitoso cuando la última tarea del DAG finalice exitosamente.
5. Realizar una carga histórica de la última semana
