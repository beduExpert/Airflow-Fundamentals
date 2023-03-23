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

from airflow import DAG
from airflow.operators.python import PythonOperator

# https://open-meteo.com/en/docs#latitude=19.43&longitude=-99.13&hourly=temperature_2m
API = "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m"

def _obtiene_temperatura_cdmx():
    return requests.get(API).json()['hourly']

def _filtra_temperatura_hoy_y_pasado(ti):
    data = ti.xcom_pull(task_ids='obtiene_temperaturas_cdmx')
    logging.info(data)
    
    hoy = datetime.today()
    futuro = hoy + timedelta(days=2)    
    hoy_iso8601 = hoy.strftime("%Y-%m-%dT%H:00")
    futuro_iso8601 = futuro.strftime("%Y-%m-%dT%H:00")
    temperatura = dict(zip(data['time'], data['temperature_2m']))
    procesado  = {k:v for k,v in temperatura.items() if k in [hoy_iso8601, futuro_iso8601]}
    ti.xcom_push(key='hoy_y_pasado_celsius', value=procesado)


def _convierte_escala_temperatura(ti):
    data = ti.xcom_pull(task_ids='filtra_temperatura_hoy_y_pasado', key='hoy_y_pasado_celsius')
    logging.info(data)
    convertido = {k: (v * 1.8) + 32  for k,v in data.items() }
    ti.xcom_push(key='hoy_y_pasado_farenheit', value=convertido)

# ① Crea una instancia del objeto DAGcon un manejador de contexto
with DAG(
    dag_id="s03_e2_temperatura",                                         # ② El nombre del DAG
    description="Ejemplo 2. Conversion de Temperatura",                     
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),            # ③ La fecha en la que el DAG deberá ejecutarse por primera vez
    schedule=None,                                                  # ④ El intervalo al que el DAG deberá ejecutarse
    tags =['ejemplo', 'tarea de flujo']
) as dag:
    obtiene_temperatura = PythonOperator(
        task_id='obtiene_temperaturas_cdmx',
        python_callable=_obtiene_temperatura_cdmx
    )

    filtra_temperatura_hoy_y_pasado = PythonOperator(
        task_id ='_filtra_temperatura_hoy_y_pasado',
        python_callable=_filtra_temperatura_hoy_y_pasado
    )

    convierte_escala = PythonOperator(
        task_id ='convierte_escala_temperatura',
        python_callable=_convierte_escala_temperatura
    )

obtiene_temperatura >> filtra_temperatura_hoy_y_pasado >> convierte_escala
