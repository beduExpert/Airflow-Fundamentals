from airflow import Dataset
import pendulum
from airflow.operators.bash import BashOperator
from airflow.decorators import dag

example_dataset = Dataset("s3://dataset/example.csv")
example_dataset_2 = Dataset("/local/input.txt")
@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def productor():
    BashOperator(task_id="productor", outlets=[example_dataset],
    bash_command="echo 'productor'")

productor()

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def productor_dos():
    BashOperator(task_id="productor_dos", outlets=[example_dataset_2],
    bash_command="echo 'productor dos'")

productor_dos()
