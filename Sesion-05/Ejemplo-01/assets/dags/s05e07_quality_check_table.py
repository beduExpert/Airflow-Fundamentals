import pendulum
from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLTableCheckOperator


@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def pruebas_calidad_nivel_tabla():
    table_checks = SQLTableCheckOperator(
        task_id="table_checks",
        conn_id="postgres",
        table="film",
        partition_clause="last_update >= '2013-02-01'",
        checks={
            "my_row_count_check": {"check_statement": "COUNT(*) >= 1000"},
            "my_column_sum_comparison_check": {
                "check_statement": "SUM(rental_duration) < SUM(rental_rate)",
                "partition_clause": "release_year > 2000",
            },
            "my_column_addition_check": {
                "check_statement": "rental_duration + rental_duration = 2*rental_duration"
            },
        },
    )
pruebas_calidad_nivel_tabla()