## Sesión 5: Nombre de sesión 🤖

### 1. Objetivos :dart: 

- Utilizar el decorador `@task.group` para organizar mejor las tareas en grupos
- Integrar tareas de control de calidad en los flujos de trabajo
- Usar el mecanismo de datasets para disparar DAGs

### 2. Contenido :blue_book:

Las liberaciones recientes de Airflow, han añadido nuevas funcionalidades que mejoran la legibilidad del código, aumentan la confiabilidad de tus flujos de trabajo y cubren escenarios en los que tienes que disparar un DAG cuando un conjunto de datos se cree o actualice.

---

#### <ins>Tema 1</ins>

En este tema comenzaremos a utilizar los agrupadores de tareas para organizar mejor nuestros DAGs.


1. Lo primero que tenemos que hacer, es importar el decorador `task_group`

    ```python
    from airflow.decorators import task_group
    ```

2. Declaramos una función Python `grupo_tareas()` ,decorado con `@task_group` y pasamos como parámetro el identificador del grupo.

    ```python
        @task_group(group_id='grupo1')
        def grupo_tareas():
            ...
    ```

3. Dentro de la función anterior, definimos:
    - las tareas que componen el grupo

    ```python
        @task(task_id='t1')
        def task_a():
            pass
        @task(task_id='t2')
        def task_b():
            pass
        @task(task_id='t3')
        def task_c():
            pass
    ```

    - y la relación de dependencia entre ellas
        - [secuencial](/Sesion-05/Ejemplo-01/assets/dags/s05e02a_grupo_tareas_decoradas_secuencial.py)

            ```python
            task_c() << task_b() << task_a()
            ```
        ![image](/Sesion-05/Ejemplo-01/assets/img/grupo_tareas_secuencial.png)
        - o en [paralelo](Sesion-05/Ejemplo-01/assets/dags/s05e02b_grupo_tareas_decoradas_paralelo.py)

            ```python
            task_a()
            task_b()
            task_c()    
            ```
        ![image](/Sesion-05/Ejemplo-01/assets/img/grupo_tareas_paralelo.png)

4. Habilita y ejecuta el DAG
5. En la vista de grafo (Graph), expande la tarea `grupo1`
6. Coloca el cursor sobre la tarea `t1` y observa el valor del `task_id`.

    ![image](/Sesion-05/Ejemplo-01/assets/img/grupo_tarea_id.png)

Podrás encontrar los ejemplos completos en el repositorio:

- [**`EJEMPLO 1.a`**](/Sesion-05/Ejemplo-01/assets/dags/s05e02a_grupo_tareas_decoradas_secuencial.py)
- [**`EJEMPLO 1.b`**](/Sesion-05/Ejemplo-01/assets/dags/s05e02a_grupo_tareas_decoradas_paralelo.py)

[**RETO 1**](/Sesion-04/Sesion-05/Reto-01/README.md): Refactorizar el ejemplo [S04_e05_ubicacion_sucursales_branch.py](/Sesion-04/Ejemplo-05/assets/dags/s04_e05_ubicacion_sucursales_branch.py), usando grupos de tareas.

---

#### <ins>Tema 2</ins>

Las pruebas de calidad son claves para el buen funcionamiento de un pipeline en un ambiente de producción, nos ayudan a validar las expectativas que tenemos sobre nuestros datos.

Necesitaremos una base de datos SQL sobre la cuál ejecutar nuestras pruebas, para ello reutilizaremos el servicio de postgres que utiliza Airflow y la base de datos de ejemplo [dvdrental](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/).

### Parte I. Descargar base de datos de ejemplo

> Nota: esta actividad se puede hacer usando el navegador web y el explorador de archivos.

1. Abrir una terminal
2. Cambiarse al directorio de trabajo

  ```bash
  cd airflow
  ```

3. Crear una carpeta de datos

  ```bash
  mkdir datos
  ```

4. Descargar la base de datos de ejemplo ["DVD Rental"](https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip)

  ```bash
  wget https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
  ```

5. El archivo esta en formato `zip`, así que tienes que descomprimirlo para obtener el archivo `dvdrental.tar`

  ```bash
  unzip dvdrental.zip
  ```

### Parte II. Compartir la carpeta de datos local con el contendor de Postgres

Ahora modificaremos `postsgres.volumes` en el archivo `docker-compose.yaml`

1. Cambiarse al directorio de trabajo, `cd airflow`
2. Detener todos los servicios, `docker-compose stop`
3. Editar el archivo `docker-compose.yaml` y agregar un nuevo volumen `/tu/carpeta/local/datos:/datos`

  ```yaml
    ...
    postgres:
      image: postgres:13
      environment:
        POSTGRES_USER: airflow
        POSTGRES_PASSWORD: airflow
        POSTGRES_DB: airflow
      volumes:
        - postgres-db-volume:/var/lib/postgresql/data
        - /tu/ruta/local/airflow/datos:/datos   #<- agregar esta línea
    ...
  ```

4. Guardar los cambios
5. Levantar los servicios `docker-compose up`
6. Utilizar VS Code + Docker plugin, para acceder y controlar el sistema del contenedor de Postgres, mediante la opción `Attach Shell` del menú contextual.
7. Se abrirá una nueva terminal que se conectará al contenedor
9. Verifica que el archivo de base de datos este disponible
    ```bash
    ls ./datos/dvdrental.tar
    ```
10. Crea la base de datos
    ```bash
    psql -U airflow
    airflow=# CREATE DATABASE dvdrental;
    airflow=# \l
    airflow=# \q
    ```
11. Restaurar la base de datos de ejemplo

  ```bash
  pg_restore \
    -U airflow \
    --no-owner \
    --role=airflow \
    --verbose \
    -d dvdrental  ./datos/dvdrental.tar
  ```

12 . Verificar que la base de datos se creo correctamente
  ```bash
  psql -U airflow -d dvdrental -c 'SELECT * FROM public.film limit 5'
  ```

## (Opcional) Conexión a Postgres usando un cliente

![image](/Sesion-05/Ejemplo-02/assets/img/vscode_postgres.png)

Es posible explorar la base de datos de postgres desde VS Code usando [PostgreSQL Management Tool](https://marketplace.visualstudio.com/items?itemName=ckolkman.vscode-postgres)

1. Abrir VS Code
2. Instalar el plug-in [PostgreSQL Management Tool](https://marketplace.visualstudio.com/items?itemName=ckolkman.vscode-postgres)

3. Editar el archivo `docker-compose.yaml` y agregar `postgres.ports` como se muestra en el siguiente extracto:

  ```yaml
    ...
    postgres:
      image: postgres:13
      ports:
        - 5432:5432
    ...
  ```

4. Reiniciar los servicos

  ```bash
  cd airflow && docker-compose restart
  ```

5. Abrir el explorador de PostgreSQL y crear una nueva conexión, usando los siguientes parámetros:

  | parámetro | valor |
  | - | - |
  | hostname | localhost|
  | user | airflow |
  | password | airflow |
  | port | 5432 |
  | ssl connection | Standard Connection |


![image](/Sesion-05/Ejemplo-02/assets/img/how_to_connect_postgres.gif)



- [**`EJEMPLO 2`**](Sesion-05/Ejemplo-02/README.md)
- [**`RETO 2`**](/Sesion-05/Reto-02/README.md)
---

#### <ins>Tema 3</ins>

Ahora que tenemos mayor conocimiento de nuestro proyecto, vamos a configurar un emulador de algún dispositivo móvil para poder correr nuestra aplicación! :iphone:. Es decir, vamos a correr un dispositivo móvil virtual en nuestra computadora para simular la funcionalidad de nuestra app.


- [**`RETO 2`**](./Reto-02)
---

<img src="images/chaomi.png" align="right" height="110"> 

#### <ins>Tema 4</ins>

Basta de emulaciones, ahora veamos como funciona en el mundo real. Nuestra app, por muy sencilla que sea ya está lista para ser instalada en un dispositivo móvil y para verla en acción.

**Nota al Experto:**
  
 + Recuerda que cada subtema puede contener un ejemplo, un reto, o más de un ejemplo y más de un reto. Recuerda borrar esta línea después de haberla leído.
- [**`RETO 3`**](./Reto-03)
---

### 3. Postwork :memo:

Encuentra las indicaciones y consejos para reflejar los avances de tu proyecto de este módulo.

- [**`POSTWORK SESIÓN 1`**](./Postwork/)

<br/>


</div>

