from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task_group, task
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def grupo_de_tareas_decoradas():
    t0 = EmptyOperator(task_id='inicio')
    @task_group(group_id='grupo1')
    def grupo_tareas():
        @task(task_id='t1')
        def task_a():
            pass
        @task(task_id='t2')
        def task_b():
            pass
        @task(task_id='t3')
        def task_c():
            pass
        task_a()
        task_b()
        task_c()                

    t3 = EmptyOperator(task_id='fin')
    t0 >> grupo_tareas() >> t3

grupo_de_tareas_decoradas()
