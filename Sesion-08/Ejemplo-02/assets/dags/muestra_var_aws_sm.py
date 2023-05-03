from airflow.decorators import dag, task
from airflow.models import Variable

import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023,4,1,tz="UTC"),
    catchup=False
)
def muestra_aws_sm_var():
    @task
    def display():
        mi_variable = Variable.get('mi_otra_variable',None)
        print(mi_variable)
    display()
muestra_aws_sm_var()
