# Ejemplo # - Notificaciones por Slack

## Objetivo

* Enviar un mensaje por Slack utilizando el operador `SlackWebhookOperator` y la conexión `slack_connection`.
* Enviar notificaciones de tareas fallidas usando una función Python de tipo callback

## Desarrollo

### Parte I

Utilizaremos la API [Free Weather API](https://open-meteo.com/) para extraer el pronóstico del clima en la Ciudad de México a las 7AM y posterioermente enviaremos esta información al canal de `#alertas` de Slack.

Este es la llamada que usaremos para comunicarnos con el API
```bash
curl  "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m" | jq | head -n25
```
Este es un extracto de la respuesta de la llamada anterior.

![image](/Sesion-06/Ejemplo-02/assets/img/open_meteo_output.png)

Así es como se mostrará el mensaje en slack
![image](/Sesion-06/Ejemplo-02/assets/img/mensaje_clima.png)

1. Creamos una nueva conexión llamada `slack_connection`, de tipo  `Slack Incoming Webhook`, utilizando la interfaz de Airflow, `Admin > Connections`
        
    - `Slack Webhook Endpoint`: https://hooks.slack.com/services/
    - `Webhook Token`: <Webhook URL>
    
    > Nota: Puedes usar el siguiente comando para verificar que el Webhook de slack funciona correctamente
    ```bash
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/<Webhook URL>
    ```

2. Creamos una archivo DAG e importamos `SlackWebhookOperator`.

    ```python
    from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
    ```

3. Instanciamos una tarea `SlackWebhookOperator` con los siguientes parámetros

    ```python
    post_daily_forecast = SlackWebhookOperator(
        task_id='post_daily_forecast',
        http_conn_id='slack_connection',
        message=get_daily_forecast()
    )
    ```

4. Escribimos una funcion de Python para consultar el API y regresar la información que necesitamos en una sola línea.

    ```python
    API = "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m"

    def get_daily_forecast() -> str:
        forecast = requests.get(API).json()['hourly']['temperature_2m'][7]
        time = requests.get(API).json()['hourly']['time'][7].split('T')[1]
        return f'La predicción de la temperatura en la Ciudad de México a las {time} es de: {forecast} °C'
    ```

5. Guardamos, activamos y ejecutamos el DAG en Airflow
6. Verificamos que el mensaje aparezcan en el canal de slack.

[s06_e02_webhook_slack.py](/Sesion-06/Ejemplo-02/assets/dags/s06_e02_webhook_slack.py)

### Parte II

![image](/Sesion-06/Ejemplo-02/assets/img/on_failure_error.png)

Ahora utilizaremos la función Python `task_fail_slack_alert` para que cada vez que una tarea sea marcada como fallida se dispare un mensaje como el anterior.

```python
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
...
def task_fail_slack_alert(context):
   slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
   slack_msg = """
           :red_circle: Task Failed.
           *Task*: {task} 
           *Dag*: {dag}
           *Execution Time*: {exec_date} 
           *Log Url*: {log_url}
           """.format(
           task=context.get('task_instance').task_id,
           dag=context.get('task_instance').dag_id,
           ti=context.get('task_instance'),
           exec_date=context.get('execution_date'),
           log_url=context.get('task_instance').log_url,
       )
   failed_alert = SlackWebhookOperator(
       task_id='slack_test',
       http_conn_id='slack_connection',
       webhook_token=slack_webhook_token,
       message=slack_msg,
       username='airflow',
       dag=dag)
   return failed_alert.execute(context=context)
```

1. Creamos un archivo DAG e instanciamos una tarea de tipo BashOperator
2. Forzamos un error ejecutando el comando `exit 1`
3. Usamos el parámetro `on_failure_callback` para pasar el nombre de la función que se ejecutará cuando la tarea falle, `task_fail_slack_alert`

    ```python
    with DAG(
    dag_id = 'test_alert_on_failure_callback',
    start_date=datetime(2023, 3, 1),
    schedule_interval='12 * * * *',
    catchup=False,
    ) as dag:
    BashOperator(
        task_id='error_forzado',
        bash_command="exit 1",
        on_failure_callback=task_fail_slack_alert)
    ```

4. Ejecutamos el DAG y revisamos el mensaje en Slack.

[Sesion-06/Ejemplo-02/assets/dags/s06_e02_call_back_failure.py](/Sesion-06/Ejemplo-02/assets/dags/s06_e02_call_back_failure.py)

