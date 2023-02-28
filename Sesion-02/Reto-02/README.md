# Reto 2. Foto de cumpleaños

## Objetivo

* Utilizar BASH operator para obtener datos de una API pública
* Practicar el uso de comandos de linux
* Familiarizarse con el formato `JSON`

## Desarrollo

¿Cuál es la foto que corresponde al día de tu cumpleaños?

La base de datos de APOD almacena todas la fotografías desde 1995, utiliza la [documentación disponible](https://api.nasa.gov/) para construir un comando bash que obtenga los datos de la fotografía que la NASA capturó el día de tu pasado cumpleaños.

1. Crear un nuevo archivo DAG
2. Declara el DAG con un nuevo nombre, `dag_id`
3. Agrega un BashOperator
4. Utiliza el comando `curl` correspondiente para descargar el archivo `JSON`
5. Comprueba que no tienes errores de sintáxis
6. Activa y ejecuta el DAG
7. Comprueba que el campo `date` dentro del arhivo `JSON` corresponde al día de tu último cumpleaños

> Sugerencia: Utiliza la terminal para probar tu comando `curl` antes de implementar el DAG

## Definición de hecho

1. Comando `curl` con los parámetros correspondientes
2. Archivo `JSON` correspondiente al día de tu pasado cumpleaños

Ejemplo:


```json
{"copyright": "Petr HoralekInstitute of Physics in Opava",
 "date": "<fecha-de-tu-pasado-cumpleaños>",
 "explanation":"Can you still see the comet? Yes.Even as C/2022 E3 (ZTF)",
 "hdurl": "https://apod.nasa.gov/apod/image/2302/ZtfDippersB_Horalek_960_annotated.jpg",
 "media_type": "image",
 "service_version": "v1",
 "title": "A Comet and Two Dippers",
 "url":"https://apod.nasa.gov/apod/image/2302/ZtfDippersB_Horalek_960_annotated.jpg"}
```