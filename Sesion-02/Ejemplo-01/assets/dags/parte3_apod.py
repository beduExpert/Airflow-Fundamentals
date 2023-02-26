from airflow import DAG
from airflow.operators.python import PythonOperator

import logging
import json
import pathlib
import pendulum
import requests
import requests.exceptions as requests_exceptions

OUTPUT_DIR = '/opt/airflow/dags/sesion02/pictures'
INPUT_DIR = '/opt/airflow/dags/sesion02/metadata'


def _descarga_foto():
    # creamos la carpeta destino si no existe
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    # recuperamos los metadatos descargados en el paso anterior
    with open(f'{INPUT_DIR}/apod.json', 'r') as f:
        info = json.load(f)
        image_url = info['url']        
        try:
            image_filename = image_url.split("/")[-1]
            target_file = f'{OUTPUT_DIR}/{image_filename}'
            logging.info(f"Descargando la foto del día {image_url} al archivo local: {target_file}")

            response = requests.get(image_url, timeout=100)
            with open(target_file, "wb") as f:
                f.write(response.content)            
        except requests_exceptions.ConnectionError:
            logging.error(f"Error de conexión {image_url}.")
    return info['title']

with DAG(
    dag_id="parte3_apod",
    description="Ejemplo 1. NASA's Astronomy Picture of the Day",                    
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),
    schedule=None
  ) as dag:
    descarga_foto = PythonOperator(
        task_id ='descarga_foto',
        python_callable = _descarga_foto
    )
