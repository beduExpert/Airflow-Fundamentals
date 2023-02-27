from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator


INCLUDE_DIR = '/opt/airflow/includes'
BUCKET_NAME = 'airflow-redshift-demostracion'
with DAG(
    dag_id=f"ejemplo_redshift",
    schedule="@daily",
    start_date=datetime(2023, 2, 24),
    max_active_runs=1,
    template_searchpath=f'{INCLUDE_DIR}/redshift',
    catchup=False
) as dag:

    query_to_s3 = RedshiftToS3Operator(
        task_id='descarga_reporte_de_ventas_de_redshift_a_s3',
        s3_bucket=BUCKET_NAME,
        s3_key='reporte/ventas/{{ ds }}_',
        select_query="""SELECT firstname, lastname, total_quantity, cast(\\'{{ ds }}\\' as date)  as ds
                        FROM   (SELECT buyerid, sum(qtysold) total_quantity
                                FROM  tickit.sales
                                GROUP BY buyerid
                                ORDER BY total_quantity desc limit 10) Q, tickit.users
                        WHERE Q.buyerid = userid
                        ORDER BY Q.total_quantity desc
        """,
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

    redshift_ddl = RedshiftSQLOperator(
        task_id='crea_tabla_datos_externos',
        sql='/ddl/datos_externos.sql',
        params={
            "schema": "tickit",
            "table": "datos_externos"
        }
    )

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

    query_to_s3 >> redshift_ddl >> s3_to_redshift