from __future__ import annotations
from uneven_intervals_timetable import UnevenIntervalsTimetable
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ejemplo_timetable",
    start_date=pendulum.datetime(2023, 2, 20, tz="UTC"),
    catchup=True,
     schedule=UnevenIntervalsTimetable()
) as dag:
    t1 = BashOperator(
        task_id="imprime_fecha",
        bash_command="echo $(date)"
    )