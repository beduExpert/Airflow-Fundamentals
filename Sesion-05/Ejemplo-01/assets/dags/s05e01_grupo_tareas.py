from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def grupo_de_tareas():
    t0 = EmptyOperator(task_id='inicio')

    with TaskGroup(group_id='grupo1') as tg1:
        t1 = EmptyOperator(task_id='tarea1')
        t2 = EmptyOperator(task_id='tarea2')
        t1 >> t2

    t3 = EmptyOperator(task_id='fin')
    t0 >> tg1 >> t3

grupo_de_tareas()
