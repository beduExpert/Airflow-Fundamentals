
from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator

import json
import pendulum

@dag(    
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def test_http_connection():
    extrae_datos = SimpleHttpOperator(
        task_id='extrae_metadatos',
        http_conn_id='HTTP_ENV_VAR',
        endpoint='/apod?api_key=DEMO_KEY',        
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )
test_http_connection()