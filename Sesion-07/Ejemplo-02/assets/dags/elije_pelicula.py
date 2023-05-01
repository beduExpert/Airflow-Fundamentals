from operators.seleccionaPeliculaOperator import NombraPelicula
from airflow.decorators import dag

import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023,4,1,tz="UTC"),
    catchup=False
)
def operador_db():
    t1 = NombraPelicula(task_id="tarea-ejemplo", 
                                postgres_conn_id='postgres',
                                genero="Drama")
operador_db()


