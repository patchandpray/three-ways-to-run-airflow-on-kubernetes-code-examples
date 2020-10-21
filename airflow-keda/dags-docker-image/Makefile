REGISTRY=
GCP_PROJECT=
IMAGE=
TAG=
PROJECT=

build:
	docker build -t ${IMAGE}:${TAG} .
	docker tag ${IMAGE}:${TAG} ${REGISTRY}/${GCP_PROJECT}/${IMAGE}:${TAG} 
	docker push ${REGISTRY}/${GCP_PROJECT}/${IMAGE}:${TAG} 

update_dags:
	helm upgrade airflow -n airflow \
		--reuse-values \
		--set images.airflow.repository=${REGISTRY}/${GCP_PROJECT}/${IMAGE} \
		--set images.airflow.tag=${TAG} \
		astronomer/airflow
