from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

OUTPUT_DIR = '/opt/airflow/dags/sesion02/pictures'

with DAG(
    dag_id="parte4_apod",
    description="Ejemplo 1. NASA's Astronomy Picture of the Day",                    
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None
  ) as dag:
  notifica = BashOperator(
    task_id="notifica",
    bash_command=f'echo "Ahora son $(ls {OUTPUT_DIR} | wc -l) fotografías."'
  )

