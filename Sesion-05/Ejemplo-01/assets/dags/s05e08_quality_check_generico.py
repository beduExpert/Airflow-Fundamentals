from airflow.operators.sql import (SQLCheckOperator, SQLIntervalCheckOperator,
                                   SQLThresholdCheckOperator,
                                   SQLValueCheckOperator)
from airflow.decorators import dag
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def pruebas_calidad_generica():
    yellow_tripdata_row_quality_check = SQLCheckOperator(
        conn_id="example_conn",
        task_id="yellow_tripdata_row_quality_check",
        sql="row_quality_yellow_tripdata_check.sql",
        params={"pickup_datetime": "2021-01-01"},
    )

pruebas_calidad_generica()