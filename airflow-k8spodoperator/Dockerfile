# take Airflow base image
FROM apache/airflow:1.10.12

# add dependencies for http basic auth
RUN pip install --user --upgrade apache-airflow[password]==1.10.12

# add dags
ADD dags /opt/airflow/dags
