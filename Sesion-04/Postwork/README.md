# Sesión #4: Mejoras de DAGs 

Después de haber completado esta sesión serás capaz de aprovechar la flexibidad que ofrece Airflow al momento de finir tus flujos de trabajos.

## 🎯 Objetivos

- Integrar los decoradores `@task`, `@dag` y `@task.branch`
- Utilizar las variables de Airflow para controlar el DAG sin tener que modificar el código
- Establecer limites de tiempo para controlar el máximo tiempo de ejecución de las tareas
## ⚙ Requisitos

+ Ambiente local de Airflow 

## Desarrollo


Como el nombre de la sesión lo indica, nos centraremos en agregar nuevas características al DAG desarrollado en el Postwork de la sesión anterior.

1. Reemplazar la definición del DAG utilizando el decorador `@dag`
2. Agregar ó reemplazar el operador `PythonOperator` por una función decorada con `@task`
3. Agregar una función de bifuración con el decorador `@task.branch`
4. Crear una variable desde la interfaz de Airflow para controlar el fjujo de tareas
5. Aplica un tiempo límite razonable a cada una de tus tareas

    > Nota: Puedes basar tu decisión en los datos generados por ejecuciones anteriors y disponbles a través de la gráfica de Gantt en la interfaz web de Airflow.

🪙 Opcional

Ya que en el prework cubrimos los pasos necesarios para configurar un servicio de correos, también podrás realizar este ejercicio localmente

1. Habilitar un servicio de correo de la nube, AWS SES o Sendgrid
2. Dar de alta un remitente/destinatario verificados en tu servicio
3. Modificar el archivo de configuración de Airflow utilizando el archivo `docker-compose.yaml` para establecer el backend y el remitente que se usará en el envío de correos
4. Crear una conexión por default para el email
5. Realizar una prueba de envío de correo utilizando el siguiente archivo DAG [/s04_e07_correo.py](/Sesion-04/Ejemplo-07/assets/dags/s04_e07_correo.py).
