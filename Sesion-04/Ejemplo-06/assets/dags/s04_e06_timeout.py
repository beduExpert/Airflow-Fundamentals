import pendulum
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from datetime import timedelta

@dag(
    schedule=None,
    catchup=False,    
    max_active_runs=1,
    start_date=pendulum.datetime(2023, 3, 4, tz="UTC"),
    default_args={"email": "airflow@example.com"}
)
def ejemplos_de_ejecucion():
    t0 = EmptyOperator(task_id='start')
    
    t1 = BashOperator(task_id='tarea_interminable',
                      bash_command='sleep 300',
                      execution_timeout=timedelta(minutes=2)
    )

    t2 = BashOperator(
        task_id='sla_forzado',
        bash_command='sleep 600',
        sla=timedelta(minutes=3)
    )

    t0 >> [t1, t2]
ejemplos_de_ejecucion()
