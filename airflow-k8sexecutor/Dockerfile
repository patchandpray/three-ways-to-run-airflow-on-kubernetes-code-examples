# take Airflow base image
FROM apache/airflow:1.10.11

# add dependencies for http basic auth
RUN pip install --user --upgrade apache-airflow[password]==1.10.11 apache-airflow[gcp]

# add dags
ADD dags /opt/airflow/dags
