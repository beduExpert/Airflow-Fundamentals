from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def pruebas_calidad_exitosa():
    check_columns = SQLColumnCheckOperator(
        task_id="check_columns",
        conn_id="postgres",
        table="film",
        column_mapping={
            "film_id": {"unique_check": {"equal_to": 0}},
            "title": {
                 "distinct_check": {"geq_to": 10},
                 "null_check": {"equal_to": 0},
             },
            "rental_duration": {
                "min": {"less_than": 100},
                "max": {"greater_than": 0, "tolerance": 0.1},
            },
        },
    )

pruebas_calidad_exitosa()