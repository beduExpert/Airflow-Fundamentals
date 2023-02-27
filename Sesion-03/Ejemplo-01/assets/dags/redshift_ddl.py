from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator


INCLUDE_DIR = '/opt/airflow/includes'
BUCKET_NAME = 'airflow-redshift-demostracion'
with DAG(
    dag_id=f"redshift_ddl",
    schedule="@daily",
    start_date=datetime(2023, 2, 24),
    max_active_runs=1,
    template_searchpath=f'{INCLUDE_DIR}/redshift',
    catchup=False
) as dag:
    redshift_ddl = RedshiftSQLOperator(
        task_id='crea_tabla_datos_externos',
        sql='/ddl/datos_externos.sql',
        params={
            "schema": "tickit",
            "table": "datos_externos"
        }
    )