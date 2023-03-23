# Reto # - Creación de tareas dinámicas

## Objetivo

Practicar el uso de tarea de flujos y tareas dinámicas.

## Desarrollo

>**💡 Nota para experto(a)**
>
> Este es un ejemplo por si el experto necesita tener en cuenta un punto clave durante el reto.
>Si no es necesario, puedes borrar esta nota.

### Introducción

Este ejemplo utiliza un endpoint público alojado en https://services.elektra.com.mx/, para utilizarlo solo debemos pasar como entrada el id del municipio y el del estado de la república.

La siguiente petición regresa la ubicación de las tiendas en formato JSON para el municipo de Alvaro Obregon (`idEstado=9` y `idMunicipio=10`)

```bash
curl -s -L "https://services.elektra.com.mx/orion_services/StoreLocation/SelfService/GetStores?idEstado=9&idMunicipio=10
```
![image](/Sesion-04/Ejemplo-03/assets/img/services_get_stores.png)
[jq_cheat_sheet](/Sesion-04/Ejemplo-03/jq-cheetsheet.md)

### Reto

Una vez que estés familiarizado con el uso del endpoint, deberás crear un DAG, utilizando los operadores @dag y @task, que obtenga en paralelo la ubicación de las sucursales de al menos 5 municipios de la Ciuadad de México.

![dag_ubicacion_sucursales_cdmx.png](/Sesion-04/Ejemplo-03/assets/img/dag_ubicacion_sucursales_cdmx.png)

Tip: Este es un DAG que realiza la misma tarea pero suando `BashOperator`. [s04_e03_ubicacion_sucursales.py](/Sesion-04/Ejemplo-03/assets/dags/s04_e03_ubicacion_sucursales.py)

