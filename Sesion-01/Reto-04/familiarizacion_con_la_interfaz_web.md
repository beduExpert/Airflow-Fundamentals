## Reto 4. Interfaz Web

La finalidad de este reto es que utilces las distintas vistas de DAG y ejecutes algunas de las acciones disponibles desde la interfaz de Airflow.

1. Tomate tu tiempo para explora el resto las vistas disponible del DAG `example_bash_operator`

- Grid
- Calendar
- Task Duration
- Landing Times
- Gantt
- Details
- Code
- Audit Log

2. Ejecuta el DAG varias veces para generar más información para enriquecer los datos para algunas de las vistas

3. En la vista de `Graph`, haz click en alguna de las tareas y forza el estado a fallido utilizando el `Task Action > Mark Failed`

4. Cambia a la vista de cuadrícula y observa los cambios de estado tanto de las tareas como del DAG.

5. Utiliza la vista `Grid` para cambiar el estado del DAG a fallido utilizando el botón `Mark Failed` que se encuentra de lado derecho.

6. Por último haz click en el icono de la cesta, para borrar los metadatos generados. 

    > Recuerda que esta acción no elimina el archivo DAG que contiene la definición de tu flujo de trabajo, solo afecta a los metadatos.

7. Revisa nuevamente cada una de las vistas para confirmar el efecto de esta última acción.
