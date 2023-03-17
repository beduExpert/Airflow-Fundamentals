# Ejecución de tu primer DAG

Ejecutaremos uno de los DAGs precargados en nuestra instalación local de Airflow: `example_bash_operator`. 

> Nota: El propósito de este DAG es demostrar las distintas maneras de usar el operador BashOperator pero por el momento no entraremos en más detalles.

1. En la interfaz de Airflow, dentro de la caja de texto `Search DAGs` escribimos la palabra “bash” (sin las comillas dobles) y presionamos ⏎ para filtrar la lista de DAGs por nombre
2. Luego movemos el cursor del mouse sobre los puntos suspensivos bajo la columna `Links`
3. En el menú flotante seleccionamos la opción `Graph`
4. De forma predeterminada todos los DAGs se encuentran en estado suspendido. Usamos el botón de activación, que aparece a la izquierda del nombre del DAG, para cambiar su estado de suspendido a activo.
5. Pulsamos el botón de ejecución [▶] , que se encuentra en el extremo derecho y luego seleccionamos la opción Trigger DAG.
6. La vista de grafo, nos permite observar el progreso de ejecución del DAG a nivel tarea y visualizar su estado final. 


