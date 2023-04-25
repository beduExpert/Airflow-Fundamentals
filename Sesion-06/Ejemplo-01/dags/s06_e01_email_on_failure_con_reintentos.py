from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

import pendulum
from datetime import timedelta

default_args = {
   "owner": "airflow",   
   "email_on_failure": False,
   "email": ["dennysregalado@hotmail.com"],
   "retries": 0
}

@dag(
    default_args=default_args,
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def notificacion_por_email_con_reintentos():
   no_envia_email = BashOperator(
      task_id="no_envia_email",
      bash_command="exit 1",
    )

   envia_email = BashOperator(
    task_id="envia_email",
    retries=2,
    retry_delay=timedelta(minutes=1),
    bash_command="exit 1",
    email_on_failure=True)

notificacion_por_email_con_reintentos()
