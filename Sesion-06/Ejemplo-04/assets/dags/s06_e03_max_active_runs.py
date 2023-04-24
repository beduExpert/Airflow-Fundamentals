from airflow.decorators import dag,task
import pendulum

from airflow.operators.bash import BashOperator

@dag(
    start_date=pendulum.datetime(2023, 4, 1, tz="UTC"),
    schedule='@daily',
    catchup=True,
    max_active_runs=1
)
def max_active_runs():
    run_this = BashOperator(
        task_id="imprime_fecha",
        bash_command="echo {{ ts }}"
    )
max_active_runs()
