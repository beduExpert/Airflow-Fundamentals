from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum  

dag = DAG(
    dag_id="parte1_apod",
    description="Ejemplo 1. NASA's Astronomy Picture of the Day",                    
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None
  )
EmptyOperator(task_id='empty', dag=dag)