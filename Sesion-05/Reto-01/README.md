# Reto #1 - Combinar @task_branch y @task_group en un mismo DAG
## Objetivo

* Uso del decorador @task_group
* Reafirmar el uso de @task_branch

## Desarrollo

1. Clonar el archivo DAG [S04_e05_ubicacion_sucursales_branch.py](/Sesion-04/Ejemplo-05/assets/dags/s04_e05_ubicacion_sucursales_branch.py)
2. Eliminar las tareas `start_region_<id>` y `end_region_<id>`
3. Crear un grupo de tareas pora region
4. Modificar la función `branch_func` para mantener la funcionalidad original

![image](/Sesion-05/Reto-01/assets/img/ubicacion-sucursales-banch-graph.png)

Resultado deseado

![image](/Sesion-05/Reto-01/assets/img/s05_r1_graph_task_group.png)
