from airflow.models import DAG
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator
from datetime import datetime



INCLUDE_DIR = '/opt/airflow/includes'
BUCKET_NAME = 'airflow-redshift-demostracion'

EXPORT_QUERY = """SELECT
        firstname,
        lastname,
        total_quantity,
        cast(\\'{{ ds }}\\' as date)  as ds
    FROM (
        SELECT buyerid, sum(qtysold) total_quantity
        FROM  tickit.sales
        GROUP BY buyerid
        ORDER BY total_quantity desc limit 10
    ) Q, tickit.users
    WHERE
        Q.buyerid = userid
    ORDER BY Q.total_quantity desc
    """

with DAG(
    dag_id=f"redshift_unload",
    schedule="@daily",
    start_date=datetime(2023, 2, 24),
    max_active_runs=1,
    template_searchpath=f'{INCLUDE_DIR}/redshift',
    catchup=False
) as dag:
    table_to_s3 = RedshiftToS3Operator(
        task_id='descarga_reporte_de_ventas_de_redshigt_a_s3',
        s3_bucket=BUCKET_NAME,
        s3_key='reporte/ventas/{{ ds }}_',
        schema='tickit',
        table='sales',
        redshift_conn_id='redshift_default',
        aws_conn_id='aws_default',
        table_as_file_name=False,
        unload_options=[
            "DELIMITER AS ','",
            "FORMAT AS CSV",
            "ALLOWOVERWRITE",
            "PARALLEL OFF",
            "HEADER"
        ]
    )

    query_to_s3 = RedshiftToS3Operator(
            task_id='descarga_reporte_de_ventas_de_redshift_a_s3',
            s3_bucket=BUCKET_NAME,
            s3_key='reporte/ventas/{{ ds }}_',
            select_query=EXPORT_QUERY,
            redshift_conn_id='redshift_default',
            aws_conn_id='aws_default',
            table_as_file_name=False,
            unload_options=[
                "DELIMITER AS ','",
                "FORMAT AS CSV",
                "ALLOWOVERWRITE",
                "PARALLEL OFF",
                "HEADER"
            ]
        )
