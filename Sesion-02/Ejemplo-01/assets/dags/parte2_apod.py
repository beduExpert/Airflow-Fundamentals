from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

OUTPUT_DIR = '/opt/airflow/dags/sesion02/metadata'

with DAG(
    dag_id="parte2_apod",
    description="Ejemplo 1. NASA's Astronomy Picture of the Day",                    
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None
  ) as dag:
    descarga_info = BashOperator(
        task_id="descarga_info",
        bash_command=f"mkdir -p {OUTPUT_DIR} && curl -o {OUTPUT_DIR}/apod.json -L 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'"
    )