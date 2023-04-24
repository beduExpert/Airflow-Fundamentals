import os
import requests

from airflow import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1),
    'retries': 0,
}
# https://api.slack.com/messaging/webhooks
# https://towardsdatascience.com/integrating-docker-airflow-with-slack-to-get-daily-reporting-c462e7c8828a#:~:text=The%20Slack%20Webhook%20Operator%20can,some%20trigger%20condition%20is%20met.
API = "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m"


def get_daily_forecast() -> str:
    forecast = requests.get(API).json()['hourly']['temperature_2m'][7]
    time = requests.get(API).json()['hourly']['time'][7].split('T')[1]
    return f'La predicción de la temperatura en la Ciudad de México a las {time} es de: {forecast} °C'

with DAG(
    dag_id='prueba_slack_webhook',
    default_args=default_args,
    start_date = datetime(2023, 3, 1),
    schedule='@daily',
    catchup=False,
) as dag:
    post_daily_forecast = SlackWebhookOperator(
        task_id='post_daily_forecast',
        http_conn_id='slack_connection',
        message=get_daily_forecast()
    )
