import logging
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

log = logging.getLogger(__name__)

dag = DAG(
    "generated_dag",
    schedule_interval="0 1 * * *",
    catchup=False,
    default_args={
        "owner": "admin",
        "depends_on_past": False,
        "start_date": datetime(2020, 8, 7),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
        "sla": timedelta(hours=23),
    },
)

with dag:

    task = KubernetesPodOperator(
        image="ubuntu:16.04",
        namespace="airflow-k8spodoperator", 
        cmds=["sleep"],
        arguments=["300"],
        labels={"foo": "bar"},
        name="downstream-task",
        task_id="task-2-sleep",
        is_delete_operator_pod=False,
        in_cluster=True,
    )

    for i in range(0, 10):
        task_name = f"generated-task-{i}"
        labels = {"task_id": i}
        task_id = f"task-{i}-echo"
        generated_task = KubernetesPodOperator(
            image="ubuntu:16.04",
            namespace="airflow-k8spodoperator", 
            cmds=["bash", "-cx"],
            arguments=["echo", "I am generated"],
            labels={"foo": "bar"},
            name=task_name,
            task_id=task_id,
            is_delete_operator_pod=False,
            in_cluster=True,
        )

        generated_task >> task
