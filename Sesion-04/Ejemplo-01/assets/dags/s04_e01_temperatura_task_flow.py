"""
    El siguiente ejemplo se conecta a uno de los APIs
    de la NASA, conocida como APOD (Astronomy Picture of the Day), 
    y descarga la imagen representativa del día y sus metadatos
    asociados
"""
import pendulum
import requests
from datetime import datetime, timedelta
import logging
from typing import Dict, Union, List  


from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task

API = "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m"


# ① Crea una instancia del objeto DAGcon un manejador de contexto
@dag(
    dag_id="s04_e01_temperatura_task_flow",
    description="Ejemplo 3. Conversion de Temperatura",
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None,
    tags =['ejemplo', 'tarea de flujo']
)
def dag():
    @task
    def obtiene_temperatura_cdmx() -> Dict[str, Union[List[str], List[float]]]:
        return requests.get(API).json()['hourly']

    @task
    def filtra_temperatura_hoy_y_pasado(data:  Dict[str, Union[List[str], List[float]]] ) ->  Dict[str, float]:
        logging.info(data)
        hoy = datetime.today()
        futuro = hoy + timedelta(days=2)    
        hoy_iso8601 = hoy.strftime("%Y-%m-%dT%H:00")
        futuro_iso8601 = futuro.strftime("%Y-%m-%dT%H:00")
        temperatura = dict(zip(data['time'], data['temperature_2m']))
        return {k:v for k,v in temperatura.items() if k in [hoy_iso8601, futuro_iso8601]}
        

    @task(timeout=timedelta(minutes=5))
    def convierte_escala_temperatura(data: Dict[str, float]) -> Dict[str, float]:
        logging.info(data)
        return {k: (v * 1.8) + 32  for k,v in data.items() }
        
    convierte_escala_temperatura(filtra_temperatura_hoy_y_pasado(obtiene_temperatura_cdmx()))
