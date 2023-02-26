"""Ejercicio 1. Estructura básica de un DAG"""
from __future__ import annotations
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hola_mundo",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
) as dag:
    run_this = BashOperator(
        task_id="imprime_fecha",
        bash_command="echo $(date)"
    )

