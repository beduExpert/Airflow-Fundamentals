"""
    El siguiente ejemplo se conecta a uno de los APIs
    de la NASA, conocida como APOD (Astronomy Picture of the Day), 
    y descarga la imagen representativa del día y sus metadatos
    asociados
"""
import json
import pathlib
import pendulum
import requests
import requests.exceptions as requests_exceptions

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

OUTPUT_DIR = '/opt/airflow/dags'

# ① Crea una instancia del objeto DAGcon un manejador de contexto
with DAG(
    dag_id="ejemplo1_apod",                                         # ② El nombre del DAG
    description="Ejemplo 1. NASA's Astronomy Picture of the Day",                     
    start_date=pendulum.datetime(2023, 1, 15, tz="UTC"),            # ③ La fecha en la que el DAG deberá ejecutarse por primera vez
    schedule=None,                                                  # ④ El intervalo al que el DAG deberá ejecutarse
    tags =['ejemplo']
) as dag:

    # ⑤ Ejecutan un comando Bash para conectarse a la API pública
    descarga_info = BashOperator(
        task_id="descarga_info",                                    # ⑥ El nombre de la tarea
        bash_command="curl -o {{ params.OUTPUT_FOLDER }}/apod.json -L 'https://go-apod.herokuapp.com/apod'",
        params = {'OUTPUT_FOLDER': OUTPUT_DIR}
    )

    # ⑦ Una funcion de Python que obtiene la url a partir de la respuesta de la API y descarga la fotografía
    def _descarga_foto():
        pathlib.Path(f'{OUTPUT_DIR}/pictures').mkdir(parents=True, exist_ok=True)
        with open(f'{OUTPUT_DIR}/apod.json', 'r') as f:
            info = json.load(f)
            image_url = info['url']
            try:
                response = requests.get(image_url, timeout=100)
                image_filename = image_url.split("/")[-1]
                target_file = f'{OUTPUT_DIR}/pictures/{image_filename}'
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Descargando la foto del día {image_url} al archivo local {target_file}")
            except requests_exceptions.ConnectionError:
                print(f"Error de conexión {image_url}.")
        return info['title']

    descarga_foto = PythonOperator(
        task_id="descarga_foto",
        python_callable=_descarga_foto                              # ⑧ LLama a la función de Python dentro del DAG con el operador PythonOpertor
    )

    notifica = BashOperator(
        task_id="notifica",
        bash_command='echo "Ahora son $(ls {{ params.OUTPUT_FOLDER }}/pictures/ | wc -l) fotografías."',
        params = {'OUTPUT_FOLDER': OUTPUT_DIR},  # Jinja2 Template
    )

    descarga_info >> descarga_foto >> notifica
