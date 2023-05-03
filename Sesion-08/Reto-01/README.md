# Reto #1 - Crear conexión a Postgres

## Objetivo

* Practicar la creación de conexiones a través de las variables de entorno

## Desarrollo

1. Modificar el archivo `docker-compose.yaml`
2. Agregar una nueva variable de conexión a postgres `DEV_CONN_ID`
3. Generar el URI y asignarlo como valor

  ```json
  "postgres": {
      "conn_type": "postgres",
      "description": "",
      "login": "airflow",
      "password": "airflow",
      "host": "postgres",
      "port": 5432,
      "schema": "dvdrental",
      "extra": ""
    }
  ``` 

4. Reiniciar los servicios de docker
5. Crear un DAG de prueba que haga referencia a la nueva conexión
6. Ejecutar el DAG para comprar que funcione correctamente.


Tip: Puedes revisar el valor de la columna `get_uri` de la tabla que regresa el comando  `airflow connections get postgres`