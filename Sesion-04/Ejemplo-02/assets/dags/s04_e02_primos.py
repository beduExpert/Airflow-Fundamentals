from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task
import pendulum

N_PRIMOS = 101
def calcula_criba():
    criba = [None,None] + (N_PRIMOS - 2)*[0]
    for i in range(2, N_PRIMOS):
        if criba[i] == 0:
            for j in range(2*i, N_PRIMOS, i):
                criba[j] = 1
    return criba
#calcula_criba()
criba = [None, None, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0,
         1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
         1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
         1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1,
         1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
         1, 1, 1]


@dag(schedule=None,
     start_date=pendulum.datetime(2023, 3, 14, tz="UTC"),
     catchup=False)
def primos():
    inicio = EmptyOperator(task_id='inicio')
    fin = EmptyOperator(task_id='fin')

    for i in range(2, len(criba)):
        if criba[i] == 0:
            task_id = f'tarea_primo_{i}'

            @task(task_id = task_id)
            def regresa_primo(valor):
                return valor
            
            inicio >> regresa_primo(i) >> fin

dag_object = primos()
if __name__== '__main__':
    dag_object.test(
        execution_date=pendulum.datetime(2023, 3, 21))
