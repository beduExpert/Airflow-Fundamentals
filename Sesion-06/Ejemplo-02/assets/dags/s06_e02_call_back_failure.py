from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

SLACK_CONN_ID = 'slack_connection'


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
       http_conn_id=SLACK_CONN_ID,
       webhook_token=slack_webhook_token,
       message=slack_msg,
       username='airflow',
       dag=dag)
   return failed_alert.execute(context=context)


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