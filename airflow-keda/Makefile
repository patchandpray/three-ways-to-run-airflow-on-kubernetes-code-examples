# This makefile can be used to deploy infrastructure to a GKE cluster

REGISTRY=
GCP_PROJECT=
IMAGE=
TAG=
PROJECT=

build:
	docker build -t ${IMAGE}:${TAG} .
	docker tag ${IMAGE}:${TAG} ${REGISTRY}/${GCP_PROJECT}/${IMAGE}:${TAG} 
	docker push ${REGISTRY}/${GCP_PROJECT}/${IMAGE}:${TAG} 

login: | configure_cluster

set_project:
	gcloud config set project ${PROJECT}

NAMESPACE=airflow
configure_cluster: authenticate
	kubectl config set-context --current --namespace=${NAMESPACE}

CLUSTER_NAME=
authenticate: 
	gcloud container clusters get-credentials ${CLUSTER_NAME} --region=europe-west1

deploy:
	kubectl apply -f k8s/namespace.yaml

helm_update:
	helm repo add kedacore https://kedacore.github.io/charts
	helm repo add astronomer https://helm.astronomer.io
	helm repo update

helm_keda: deploy 
	helm install keda \
		--namespace keda kedacore/keda

helm_airflow:
	helm install airflow \
		--set executor=CeleryExecutor \
    --set workers.keda.enabled=true \
    --set workers.persistence.enabled=false \
		--namespace airflow \
    astronomer/airflow

airflow_service:
	kubectl port-forward svc/airflow-webserver 8080:8080

flower_service:
	kubectl port-forward svc/airflow-flower 5555:5555

IP=$(shell kubectl get svc airflow-svc -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
get_url:
	echo http://${IP}/admin
	

