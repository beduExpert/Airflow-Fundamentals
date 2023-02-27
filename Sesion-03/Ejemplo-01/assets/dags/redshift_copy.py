from airflow.models import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

from datetime import datetime

INCLUDE_DIR = '/opt/airflow/includes'
BUCKET_NAME = 'airflow-redshift-demostracion'
with DAG(
    dag_id=f"redshift_copy",
    schedule="@daily",
    start_date=datetime(2023, 2, 24),
    max_active_runs=1,
    template_searchpath=f'{INCLUDE_DIR}/redshift',
    catchup=False
) as dag:
    s3_to_redshift = S3ToRedshiftOperator(
        task_id='carga_archivo_de_s3_a_redshift',
        schema='tickit',
        table='datos_externos',
        s3_bucket=BUCKET_NAME,
        s3_key='reporte/ventas/',
        redshift_conn_id='redshift_default',
        aws_conn_id='aws_default',
        copy_options=[
            "DELIMITER AS ','",
            "IGNOREHEADER 1"
        ],
        method='REPLACE'
    )