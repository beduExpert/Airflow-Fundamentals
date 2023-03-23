"""Ejemplo de ejeucución de un script bash que
utiliza una variable de entorno para construir
la URL"""
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task
from airflow.models import Variable
import pendulum


grupo_regiones = {1 : [2,3,4,5],
                  2 : [6,7,8,9],
                  3 : [10,11,12,13],
                  4 : [14,15,16,17]}
@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    catchup=False
)
def ubicacion_sucursales_banch():
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule='all_done')

    @task.branch(task_id='branch_task')
    def branch_func():
        regiones = Variable.get('regiones',  deserialize_json=True)
        return [f'start_region_{region_id}' for region_id in grupo_regiones.keys() if region_id in regiones]
    
    branch_op = branch_func()
    start >> branch_op
    for region_id, municipios in grupo_regiones.items():
        start_region = EmptyOperator(task_id=f'start_region_{region_id}')
        end_region = EmptyOperator(task_id=f'end_region_{region_id}')
        branch_op >> start_region
        for id in municipios:
            task_instance = BashOperator(
                task_id=f'municipo_{id}',
                bash_command=f'curl -s -L "https://services.elektra.com.mx/orion_services/StoreLocation/SelfService/GetStores?idEstado=9&idMunicipio={id}"')
            start_region >> task_instance >> end_region
        end_region >> end
ubicacion_sucursales_banch()
