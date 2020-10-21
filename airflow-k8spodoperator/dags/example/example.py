import logging
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

log = logging.getLogger(__name__)

dag = DAG(
    "example_using_k8s_pod_operator",
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
    task_1 = KubernetesPodOperator(
        image="ubuntu:16.04",
        namespace="airflow-k8spodoperator", 
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        name="test-using-k8spodoperator-task-1",
        task_id="task-1-echo",
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_2 = KubernetesPodOperator(
        image="ubuntu:16.04",
        namespace="airflow-k8spodoperator", 
        cmds=["sleep"],
        arguments=["300"],
        labels={"foo": "bar"},
        name="test-using-k8spodoperator-task-2",
        task_id="task-2-sleep",
        is_delete_operator_pod=False,
        in_cluster=True,
    )

task_1 >> task_2
