# Reto # - Mensajes de éxito por Slack

## Objetivo

* Consolidar el conocimiento adquirido sobre las notificaciones personalizadas por Slack

## Desarrollo

Crear una funcion `task_success_slack_alert` que se dispare cuando una tarea se complete de manera exitosa.

1. Clon el ejemplo [s06_e02_call_back_failure.py](/Sesion-06/Ejemplo-02/assets/dags/s06_e02_call_back_failure.py) y renombralo
2. Agrega la nueva función `task_success_slack_alert`
3. Agrega una tarea de tipo `EmptyOperator`
4. Usa el parámetro `on_success_callback = task_success_slack_alert`
5. Ejecuta el DAG
6. Verifica que el nuevo mensaje se dispare solo cuando la tarea sea exitosa

**Tips:**

- Usa como base la funciónnn `task_fail_slack_alert` de ejemplo
- Usa el [Block Kit builder](https://app.slack.com/block-kit-builder/T04RZB8PQCA#%7B%22blocks%22:%5B%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22:red_circle:%20Task%20Failed.%5Cn*Task*:%20task%20%5Cn*Dag*:%20dag%5Cn*Execution%20Time*:%5Cnexec_date%5Cn*Log%20Url*:%20log_url%22%7D%7D%5D%7D) de Slack para crear tu mensaje de forma interactiva

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
