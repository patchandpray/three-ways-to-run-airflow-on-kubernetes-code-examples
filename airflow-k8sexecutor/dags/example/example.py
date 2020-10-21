import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

log = logging.getLogger(__name__)

dag = DAG(
    "example_using_k8s_executor",
    schedule_interval="0 1 * * *",
    catchup=False,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2020, 8, 7),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
        "sla": timedelta(hours=23),
    },
)

def use_airflow_binary():
    rc = os.system("airflow -h")
    assert rc == 0

with dag:
    task_1 = PythonOperator(
        task_id="task-1",
        python_callable=use_airflow_binary,
    )
    task_2 = PythonOperator(
        task_id="task-2",
        python_callable=use_airflow_binary,
    )

task_1 >> task_2
