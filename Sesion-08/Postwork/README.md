# Sesión #8: Seguridad

## :dart: Objetivos

- Crear y organizar los usuarios que conforman tu equipo de acuerdo a tus necesidades específicas.

- Almacenar al menos dos de las conexiones que creaste usando la interfaz web de Airflow en AWS Secrets Manager.

## ⚙ Requisitos

+ Local Airflow

## Desarrollo

Parte I. Usuarios en tu organización

1. Definir una lista de usuarios y asignar el rol correspondiente

    Tip: Puedes asignar los roles de Airflow en base al rol funcional de los integrantes del equipo.

    | Usuario | Rol en el equipo | Rol en Airflow |
    |-|-|-|
    ||Ingeniero de Datos| Op|
    ||Lider del equipo| Admin|
    ||Analista de Datos| Viewer|

2. Crear usuarios y asignar el rol correspondiente


Parte II. Migrar conexiones a AWS Secret Manager

> Puntos extras: Utilizar conexiones y DAGs propios creados en los post-works

1. Selecciona un par de conexiones existentes en tu ambiente de Airflow
2. Recrea esas mismas coneciones en AWS Secret Manager
3. Elimina las conecciones en el ambiente de Airflow
4. Ejecuta los DAGs que utilizan esas conexiones para corroborar que sigan funcionando correctamente.
