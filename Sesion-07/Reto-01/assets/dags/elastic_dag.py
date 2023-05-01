from airflow import DAG
from airflow.operators.python import PythonOperator
from elastic_hook import ElasticHook
from airflow.decorators import task

from datetime import datetime
import json

def _print_es_info():
    #None
    hook = ElasticHook()
    print(hook.info())
 
with DAG('elastic_dag', start_date=datetime(2022, 1, 1), schedule_interval='@daily', catchup=False) as dag:
 
    print_es_info = PythonOperator(
        task_id='print_es_info',
        python_callable=_print_es_info
    )


    @task
    def agrega_libro():
        hook = ElasticHook()
        new_book = {
            "title": "Data Pipelines With Apache Airflow",
            "category":"Orchestrator",
            "published_date":"April 2021",
            "author":"Bas P. Harenslak"
        }

        res = hook.add_doc(
            index='catalog',            
            id='1005',
            doc=new_book
        )
        print(res)
    
    @task
    def consulta_libro():
        hook = ElasticHook()
        res = hook.get_doc(index='catalog', id='1005')
        print(res)

    print_es_info >> agrega_libro() >> consulta_libro()