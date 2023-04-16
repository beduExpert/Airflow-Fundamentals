import pendulum
from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator


@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def pruebas_calidad_clausula_particion():
    column_checks = SQLColumnCheckOperator(
        task_id="column_checks",
        conn_id="postgres",
        table="film",
        partition_clause="release_year = 2006",
        column_mapping={
            "rental_rate": {"min": {"greater_than": 5}},
            "length": {
                "max": {"less_than": 90, 
                        "partition_clause": "rating = 'R'"}
            },
        },
    )

pruebas_calidad_clausula_particion()
