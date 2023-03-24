
import pendulum
from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False
)
def correo(email = "airflow@example.com"):    
    EmailOperator(        
        task_id="send_email",
        to=email, 
        subject='Airflow Alert',
        html_content=""" <h3>Email Test</h3> """,
    )

example_dag = correo()