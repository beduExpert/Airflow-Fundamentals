from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

import json
import pandas as pd
import pendulum


@dag(    
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def sensor_basico():


    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS apod (
                copyright text,
                date date,
                explanation text,
                hdurl text,
                media_type text,
                service_version text,
                title text,
                url text
            );
        '''
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
        soft_fail=True
    )
    
    extrae_datos = SimpleHttpOperator(
        task_id='extrae_metadatos',
        http_conn_id='http_default',
        endpoint='/apod?api_key=DEMO_KEY',        
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )
    
    @task()
    def almacena_datos(data):
        df_single_row = pd.json_normalize(data)
        # abrir el worker y listar el archivo para comprobar
        df_single_row.to_csv('/tmp/apod.csv', index=False)
    
    t_procesa = almacena_datos(extrae_datos.output)
    create_table >> revisa_disponibilidad_api >> extrae_datos >> t_procesa
sensor_basico()
