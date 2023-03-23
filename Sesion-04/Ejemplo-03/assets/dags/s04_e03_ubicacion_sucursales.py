"""Ejemplo de ejeucución de un script bash que
utiliza una variable de entorno para construir
la URL"""
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.decorators import dag
import pendulum


@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    catchup=False,    
)
def ubicacion_sucursales_cdmx():
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')
    for id in list(range(2,10)):
        # task_instance = BashOperator(
        #     task_id=f'municipo_{id}',
        #     # el espacio al final del comando es importante!
        #     # https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html#troubleshooting
        #     bash_command="$AIRFLOW_HOME/includes/scripts/get_stores.sh ",              
        #     env={"MUNICIPIO": str(id)},
        #     append_env=True,
        # )
        task_instance = BashOperator(
            task_id=f'municipo_{id}',
            bash_command=(f'curl -s -L '
                          '"https://services.elektra.com.mx/orion_services/StoreLocation/SelfService/GetStores?idEstado=9&idMunicipio={id}"')
        )
        start >> task_instance >> end
        
ubicacion_sucursales_cdmx()
