# Reto #4 - Sensor

## Objetivo

* Explorar modo `reschedule` de un sensor: `HttpSensor`.

## Desarrollo

![image](/Sesion-05/Ejemplo-04/assets/img/sensor_fallido.png)

En este reto tendrás que utilizar el archivo DAG [s05e12_sensor_http.py](Sesion-05/Ejemplo-04/assets/dags/s05e12_sensor_http.py) y realizar los siguientes cambios:

Cambiar el modo del sensor `revisa_sensor_http` de `poke` a `reschedule` y ajustar los parámetros necesarios.

> Nota: puedes consultar el Tema #2. Sensores del prework para refrescar los conceptos.

1. Crea un nuevo archivo DAG y cambia el `dag_id`
2. Modifica la tarea `revisa_disponibilidad_api`
    - Usar el modo `reschedule` en lugar `poke`
    - Elimina aquellas configuraciones que no apliquen al modo seleccionado
3. Guarda y ejecuta el DAG
4. Consulta el log de la tarea `revisa_disponibilidad_api` y observa sucomportamiento.
    - ¿Cuál es la principal diferencia entre los dos modos de ejecución?
5. Imagina un caso de uso para cada modo y descríbelo de forma breve
  