## Sesión 4: Mejora de DAGs 🤖

### 1. Objetivos :dart: 

- Utilizar tareas de flujo con el decorador @task
- Variables de Airflow
- Crear tareas de forma dinámica

### 2. Contenido :blue_book:


---


#### <ins>Tema 1</ins>

Vamos a usar tareas de flujo para refactorizar el DAG [s03_e2_temperatura](/Sesion-03/Ejemplo-02/assets/dags/temperatura.py), de esta manera simplificamos el código haciéndolo fácil de leer y mantener.

1. Lo primero que tenemos que hacer, es importar los decoradores

    ```python
    from airflow.decorators import dag, task
    ```

2. Reemplazamos el gestor de contexto y en su lugar usamos el decorador @dag

```python
# versión con gestor de contexto
with DAG(
    dag_id="s03_e2_temperatura",
    description="Ejemplo 2. Conversion de Temperatura",                     
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None,    
) as dag:
```

```python
# versión con decorador dag
@dag(
    dag_id="s04_e01_temperatura_task_flow",
    description="Ejemplo 3. Conversion de Temperatura",
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None,
    tags =['ejemplo', 'tarea de flujo']
)
def dag():
```

3. Refactorizamos la tarea `obtiene_temperaturas_cdmx`,  solo nos quedamos con la definición de la función que realiza la solicitud al API y decoramos la función con `@task`.

    ```python
    # versión con PythonOperator
    def _obtiene_temperatura_cdmx():
        return requests.get(API).json()['hourly']

    obtiene_temperatura = PythonOperator(
        task_id='obtiene_temperaturas_cdmx',
        python_callable=_obtiene_temperatura_cdmx
    )
    ```

    ```python
    # versión con @task decorator
    @task
    def obtiene_temperatura_cdmx():
        return requests.get(API).json()['hourly']
    ```

    > Nota: el nombre de la función se convierte en el valor del `task_id`

4. Ahora es el turno de la tarea `filtra_temperatura_hoy_y_pasado` hacemos los propio y agregamos el parámetro `data` como argumento de la función!

    ```python
    # versión con PythonOperator
    def _filtra_temperatura_hoy_y_pasado(ti):
        data = ti.xcom_pull(task_ids='obtiene_temperaturas_cdmx')
        logging.info(data)
        
        hoy = datetime.today()
        futuro = hoy + timedelta(days=2)    
        hoy_iso8601 = hoy.strftime("%Y-%m-%dT%H:00")
        futuro_iso8601 = futuro.strftime("%Y-%m-%dT%H:00")
        temperatura = dict(zip(data['time'], data['temperature_2m']))
        procesado  = {k:v for k,v in temperatura.items() if k in [hoy_iso8601, futuro_iso8601]}
        ti.xcom_push(key='hoy_y_pasado_celsius', value=procesado)


    filtra_temperatura_hoy_y_pasado = PythonOperator(
        task_id ='_filtra_temperatura_hoy_y_pasado',
        python_callable=_filtra_temperatura_hoy_y_pasado
    )
    ```

    ```python
    # versión con @task decorator
    @task
    def filtra_temperatura_hoy_y_pasado(data):
        logging.info(data)
        hoy = datetime.today()
        futuro = hoy + timedelta(days=2)    
        hoy_iso8601 = hoy.strftime("%Y-%m-%dT%H:00")
        futuro_iso8601 = futuro.strftime("%Y-%m-%dT%H:00")
        temperatura = dict(zip(data['time'], data['temperature_2m']))
        return {k:v for k,v in temperatura.items() if k in [hoy_iso8601, futuro_iso8601]}
        
    ```

5. En la última tarea, `convierte_escala_temperatura`, hacemos lo mismo. 

    > Nota: Ya no es necesario realizar las operaciones `pull` y `push`, ya que el decorador se encarga de eso por nosotros.

    ```python
    # versión con PythonOperator
    def _convierte_escala_temperatura(ti):
        data = ti.xcom_pull(task_ids='filtra_temperatura_hoy_y_pasado', key='hoy_y_pasado_celsius')
        logging.info(data)
        convertido = {k: (v * 1.8) + 32  for k,v in data.items() }
        ti.xcom_push(key='hoy_y_pasado_farenheit', value=convertido)


    convierte_escala = PythonOperator(
        task_id ='convierte_escala_temperatura',
        python_callable=_convierte_escala_temperatura
    )
    ```

    ```python
    # versión con @task decorator
    @task
    def convierte_escala_temperatura(data):
        logging.info(data)
        return {k: (v * 1.8) + 32  for k,v in data.items() }
    ```

6. Por último, "encadenamos" las funciones en el orden correcto:

    - la función más interna se ejecutará primero
    - la salida de la función interna se convierte en la entrada de la función externa

    ```python
    # versión con desplazamiento de bits
    obtiene_temperatura >> filtra_temperatura_hoy_y_pasado >> convierte_escala
    ```

    ```python
    # versión con flujos de tareas
    convierte_escala_temperatura(
        filtra_temperatura_hoy_y_pasado(
            obtiene_temperatura_cdmx()))
    ```

7. Agregamos la versión refactorizada a la carpeta `dags` de nuestro ambiente local de Airflow

8. Usamos la vista de grafo (Graph) para comprobar que la dependencia entre las tareas sigue siendo correcta.

9. Activamos y ejecutamos el DAG `s04_e01_temperatura_task_flow`

10. Revisamos la salida XCom de cada una de las tareas y comprobamos que el resultado sea el esperado.


El resultado completo de esta refactorización la encontrarás en el archivo [temperatura_con_task_flow.py](/Sesion-04/Ejemplo-01/assets/dags/s04_e01_temperatura_con_task_flow.py)


---

#### <ins>Tema 2</ins>

Construiremos juntos un flujo de trabajo dinámico usando un la estructura de control de flujo `for`.

El objetivo es crear una tarea por cada número primo menor que 100. 

> Nota: Un número primo es aquel número entero mayor que 1 que solo es divisible por 1 y por sí mismo, es decir, no tiene más divisores que esos dos.

Estos son los 25 números primos que cumplen el criterio anterior:

`2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 41 | 43 | 47 | 53 | 59 | 61 | 67 | 71 | 73 | 79 | 83 | 89 | 97`

Así es como debe lucir el DAG:
![image](/Sesion-04/Ejemplo-01/assets/img/dag_primos.png)

- Las tareas de los primos deben:
    - ejecutarse después de que la tarea inicio se haya completado exitosamente
    - ejecutarse en paralelo
    - usar el siguiente plantilla de nombre `tarea_primo_{numero}`
    - compartir su valor a través del XCom
- La tarea `fin` se debe ejecutar después de que las 25 tareas hayan sido completadas exitosamente.

> En vez de usar la lista de número de primos usaremos la [criba de Eratostenes](https://www.superprof.es/diccionario/matematicas/aritmetica/criba-eratostenes.html), que en resumen es una lista de `0s` y `1s` precalculada en donde la presencia de un `0` en la `i`-esima posición de la lista indica que `i` es número primo.

1. Definimos la criba

    ```bash
    criba = [None, None, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0,
            1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
            1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
            1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1,
            1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
            1, 1, 1]
    ```

2. Creamos la función primos decorada

```python
@dag(schedule=None,
     start_date=pendulum.datetime(2023, 3, 14, tz="UTC"),
     catchup=False)
def primos():
```

3. Creamos la tarea `inicio` y `fin` usando `EmptyOperator`

    > `from airflow.operators.empty import EmptyOperator`

    ```python
    inicio = EmptyOperator(task_id='inicio')
    fin = EmptyOperator(task_id='fin')  
    ```

4. Definimos un ciclo `for` para recorrer la lista `criba`, usamos la variable `task_id` para almacenar el nombre de la tarea, y creamos una funcion con @task

    ```python
    for i in range(2, len(criba)):
        if criba[i] == 0:
            task_id = f'tarea_primo_{i}'

            @task(task_id = task_id)
            def regresa_primo(valor):
                return valor

            inicio >> regresa_primo(i) >> fin
    ```

     > IMPORTANTE: Definimos la dependencia de tareas dentro del ciclo!

Podrás encontrar el ejemplo completo en el archivo DAG [s04_e02_primos.py](/Sesion-04/Ejemplo-02/assets/dags/s04_e02_primos.py)


- [**`RETO 1`**](/Sesion-04/Reto-01/README.md)


---

#### <ins>Tema 3</ins>

En este tema ejemplificaremos el concepto de las Variables de Airflow. Para ello actualizaremos el ejemplo [s04_e03_ubicacion_sucursales.py](/Sesion-04/Ejemplo-03/assets/dags/s04_e03_ubicacion_sucursales.py) para que lea la lista de municipios a partir de una variable.

1. Lo primero que tenemos que hacer es crear la variable usando la interfaz web de Airflow. Vamos a `Admin > Variables`, hacemos clicke en el botón `[+]`
2. Creamos la variable `municipios` con los valores que muestra la siguiente imágen (última fila)
    ![image](/Sesion-04/Ejemplo-04/assets/img/variable_municipios.png)

3. Creamos un nuevo archivo DAG
4. Ahora importamos la clase `Variable`

    ```python
    from airflow.models import Variable
    ```

5. Leemos la variable

    ```python
        lista_municipios = Variable.get("municipios", deserialize_json=True)
    ```

6. Cambiamos nuestro bucle `for` para que lea los ids desde esta lista

    ```python
        for id in lista_municipios
            ...
    ```

7. Activamos y revisamos el efecto de los cambios en la vista de grafo
8. Editamos el valor de la variable `municipios` a través de la interfaz, `Admin > Variables`, ejemplo: `[2,4,8,10,12]`
9. Regresamos a la vista grafo y revisamos nuestro DAG

El archivo DAG [s04_e04_ubicacion_sucursales_variable.py](/Sesion-04/Ejemplo-04/assets/dags/s04_e04_ubicacion_sucursales_variable.py) contiene el ejemplo completo.


- [**`RETO 1`**](/Sesion-04/Reto-02/README.md)

En este reto complementarás el reto anterior usando una objeto JSON más complejo como variable de entrada.

---

#### <ins>Tema 4</ins>

Ahora aprenderemos a cambiar el comportamiento predeterminado del flujo de las tares. En este ejemplo usaremos:

- el decorador `@task.branch` para decidir qué conjunto de tareas sucesoras se ejecutarán
- cambiar la regala de disparo, `trigger_rule`, de la última tarea para que se ejecute independientemente del estado final de sus predecesores.

En este [ejemplo](/Sesion-04/Ejemplo-05/assets/dags/s04_e05_ubicacion_sucursales_branch.py) crearemos 4 ramas, una por cada region, las cuáles a su vez tendrán otras 4 ramas para cada municipio/alcaldía de la ciuadad de México.

![image](/Sesion-04/Ejemplo-05/assets/img/branch_task.png)

1. Creamos una variable nueva llamda `regiones`, `Admin > Connections`, utilizando el siguiente valor: `[1,2]`, cuyo objetivo será seleccionar cúal de las regiones se ejecutarán.

    > Aquellas regiones no seleccionadas se omitirán (estado `skipped`), este estado se propagará a través de todos los descencientes (municipios)

2. Definimos una función de bifurcación utilizando el decorador `@task.branch`

    > `from airflow.decorators import task`

    ```python
    @task.branch(task_id='branch_task')
        def branch_func():
            regiones = Variable.get('regiones',  deserialize_json=True)
            return [f'start_region_{region_id}'
                    for region_id in grupo_regiones.keys()
                    if region_id in regiones]
    ```

3. Después modificaremos la regla de disparo de la tarea `end` para que se ejecute cuando todas sus tareas predecesoras esten completadas.

    ```python
    end = EmptyOperator(task_id='end', trigger_rule='all_done')
    ```

Aquí encontrarás la versión completa del archivo DAG [s04_e05_ubicacion_sucursales_branch.py](/Sesion-04/Ejemplo-05/assets/dags/s04_e05_ubicacion_sucursales_branch.py)


- [**`RETO 3`**](./Reto-03)
---

Modifica el reto anterior, agregando una tarea de bifurcación padre que decidia qué sucursales se ejecutarán dependiendo de valor del id del municipio.

> Por ejemplo: Si el `id` es par se ejecuta, de lo contrario se omite.

### 3. Postwork :memo:

Encuentra las indicaciones y consejos para reflejar los avances de tu proyecto de este módulo.

- [**`POSTWORK SESIÓN 1`**](./Postwork/)

<br/>


</div>

