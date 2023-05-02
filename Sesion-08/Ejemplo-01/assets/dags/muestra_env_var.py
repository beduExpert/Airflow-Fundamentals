from airflow.decorators import dag, task
from airflow.models import Variable

import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023,4,1,tz="UTC"),
    catchup=False
)
def muestra_env_var():
    @task
    def display():
        mi_variable = Variable.get('MI_VARIABLE',None)
        print(mi_variable)
    display()
muestra_env_var()
