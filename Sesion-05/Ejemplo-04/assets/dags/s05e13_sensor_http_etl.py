from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import json
import pandas as pd
import pendulum


@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
    ,user_defined_macros={'json': json}
)
def etl_basic_sensor():
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql=[#'DROP TABLE IF EXISTS apod',
             '''
            CREATE TABLE IF NOT EXISTS apod (
                copyright text,
                "date" text,
                explanation text,
                hdurl text,
                media_type text,
                service_version text,
                title text,
                url text
            );
        ''']
    )

    revisa_disponibilidad_api = HttpSensor(
        task_id='revisa_sensor_http',
        endpoint='/apod',
        http_conn_id='http_default',
        request_params={'api_key':'DEMO_KEY'},
        mode='poke',
        poke_interval=30,
        timeout=120,
        response_check=lambda response: "copyright" in response.text,
        #response_check=lambda response: "httpbin" in response.text,
        soft_fail=True
    )
    
    extrae_datos = SimpleHttpOperator(
        task_id='extrae_metadatos',
        http_conn_id='http_default',
        endpoint='/apod?api_key=DEMO_KEY',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
    #    log_response=True
    )
    
    @task()
    def guarda_archivo(data):
        df_single_row = pd.json_normalize(data)       
        df_single_row.to_csv('/tmp/apod.csv', 
                             sep='|',
                             index=False)
    
    @task()
    def almacena_datos_de_archivo():
        hook = PostgresHook(postgres_conn_id='postgres')
        hook.copy_expert(
            sql="COPY apod FROM stdin WITH DELIMITER as '|' CSV HEADER",
            filename='/tmp/apod.csv'
        )
    
    
    create_table >> revisa_disponibilidad_api >> extrae_datos  >> guarda_archivo(extrae_datos.output)  >> almacena_datos_de_archivo()
etl_basic_sensor()
