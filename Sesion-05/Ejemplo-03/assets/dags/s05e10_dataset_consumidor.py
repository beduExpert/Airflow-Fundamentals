from airflow import Dataset
import pendulum
from airflow.operators.bash import BashOperator
from airflow.decorators import dag

example_dataset = Dataset("s3://dataset/example.csv")

@dag(
    schedule=[example_dataset],
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def consumidor():
    BashOperator(task_id='inicio',
                 bash_command='echo "consumidor"')

consumidor()
