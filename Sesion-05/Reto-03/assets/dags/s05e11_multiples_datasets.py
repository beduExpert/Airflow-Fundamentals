from airflow import Dataset
import pendulum
from airflow.operators.bash import BashOperator
from airflow.decorators import dag

example_dataset_1= Dataset("s3://dataset/example.csv")
example_dataset_2 = Dataset("/local/input.txt")

@dag(    
    schedule=[
        example_dataset_1,
        example_dataset_2
    ],
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def consumidor_multiple():
    BashOperator(task_id='inicio',
                bash_command='echo "consumidor múltiple"')

consumidor_multiple()
