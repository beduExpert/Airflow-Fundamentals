# Sesión #05: Mejora de DAGs

## :dart: Objetivos

- Organizar tareas comunes en grupos de tareas
- Agregar pruebas de calidad a un flujo de trabajo existente
- Encadenar DAGs por medio de un Dataset

## ⚙ Requisitos

- Ambiente local de Airflow
- Visual Studio Code
- Base de datos dvdrental en Postgres

## Desarrollo

### Parte I

Supongamos que necesitamos dar de alta un nueva película en la base de datos `dvdrental`.

Después de estudiar el diagrama ER, nos damos cuante que necesitamos modificar las siguientes tablas en el siguiente orden:

| dag | grupo | tabla |
| - | - | - |
| productor | independiente | `public.actor` |
| productor | independiente | `public.category` |
| productor | independiente | `public.language` |
| productor | dependiente | `public.film` |
| consumidor | n/a | `public.film_category` |
| consumidor | n/a | `public.film_actor` |

Para completar esta tarea vamos a usar dos DAGs, uno para modificar las tablas 1-4 y un segundo para modificar las últimas dos.

1. Crear un DAG con las siguientes características
    - Tres tareas agrupadas bajo el nombre de `independiente`, cada una de ellas deberá insertar un registro en las siguientes tablas:
        - `public.actor`
        - `public.category`
        - `public.language`
    - Una tarea bajo el grupo `dependiente` que se ejeucute inmediatamente después de que el grupo `dependiente` termine.
    - Utiliza un `EmptyOperator` para actualizar un dataset

2. Crear un segundo DAG que consuma el dataset creado y que contenga dos tareas en paralelo:
    - una tarea crear una entrada en la tabla `public.film_category`
    - y otra para hacer lo propio en la tabla `public.film_actor`
Diagram entidad relación

> Nota: Para completar este ejercio puedes usar el operador [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/5.4.0/operators/postgres_operator_howto_guide.html)


![image](/Sesion-05/Postwork/assets/img/dvd-rental-sample-database-diagram.png)

Estos son ejemplos de sentencias DML que puedes usar para realizar las inserciones.

```sql
--category
insert into public.category (name, last_update) values('Superheroe',current_date);
```

```sql
--actor
insert into public.actor (first_name, last_name, last_update) 
values('Tenoch','Huerta',current_date);
```

```sql
--language
insert into public.language (name, last_Update) values('Spanish',current_date);
```

```sql
--film
insert into public.film (title, description, release_year, 
                         language_id, rental_duration,rental_rate,
                         length,
                         replacement_cost,
                         rating,
                         last_update,
                         special_features,
                         fulltext)
select 
    'Pantera Negra: Wakanda por siempre',
    'El pueblo de Wakanda lucha para proteger su hogar de las potencias mundiales interventoras mientras lloran la muerte de su rey TChalla.',
    2022,
    language_id,
    4,
    3.99,
    161,
    20,
    'G',
    current_date,
    array['Traillers'],
    '''hello'':1 ''world'':2'::tsvector
from public.language
where name = 'Spanish';
```

```sql
-- film category
insert into public.film_category (film_id, category_id, last_update)
select 
    film_id, 
    category_id,
    current_date 
from public.film, public.category 
where 
    title = 'Pantera Negra: Wakanda por siempre'
    and name ='Superheroe'
;
```

```sql
--film_actor
insert into public.film_actor (actor_id, film_id, last_update)
select    
    actor_id,
    film_id,
    current_date
from public.film, public.actor
where 
    title = 'Pantera Negra: Wakanda por siempre'
    and first_name = 'Tenoch'
;
```

Si es necesario, puedes utilizar el siguiente script para eliminar los registros instertados.

```sql

--deletions
with t2 as (
    select 
        fc.film_id, fc.category_id     
    from public.film_category fc
        inner join public.film f
            on (fc.film_id = f.film_id)
        inner join public.category a
            on (fc.category_id = a.category_id)
    where
        title = 'Pantera Negra: Wakanda por siempre'
        and name = 'Superheroe'
)
delete from public.film_category fc
using t2
where
    fc.film_id = t2.film_id
    and fc.category_id = t2.category_id;


with t2 as (
    select 
        fa.film_id, fa.actor_id     
    from public.film_actor fa
        inner join public.film f
            on (fa.film_id = f.film_id)
        inner join public.actor a
            on (fa.actor_id = a.actor_id)
    where
        title = 'Pantera Negra: Wakanda por siempre'
        and first_name = 'Tenoch'
)
delete from public.film_actor fa
using t2
where
    fa.film_id = t2.film_id
    and fa.actor_id = t2.actor_id;

delete from public.film where title='Pantera Negra: Wakanda por siempre';
delete from public.actor where first_name='Tenoch';
delete from public.category where name='Superheroe';
delete from public.language where name='Spanish';
```

### Parte II. Pruebas de calidad

Agregar las siguientes pruebas de calidad al primer DAG para asegurar que los nuevos datos cumplen las expectativas.

>Nota: Puedes hacerlo con una o varias tareas de tipo [SQLColumnCheckOperator](https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/operators.html#check-sql-table-columns).

- el año de liberación de la película no puede no puede ser mayor a 2023
- el apellido de los actores no puede ser nulo
- la duración de la película no puede ser menor a 60 minutos
- el costo del reemplazo de la películar debe ser mayor a cero
- el rating de las películas debe ser mayor a 5

