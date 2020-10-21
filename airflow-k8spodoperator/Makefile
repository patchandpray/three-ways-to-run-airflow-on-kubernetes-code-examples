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

NAMESPACE=airflow-k8spodoperator
configure_cluster: authenticate
	kubectl config set-context --current --namespace=${NAMESPACE}

CLUSTER_NAME=
authenticate: 
	gcloud container clusters get-credentials ${CLUSTER_NAME}

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/serviceaccount.yaml
	kubectl apply -f k8s/role.yaml
	kubectl apply -f k8s/rolebinding.yaml
	kubectl apply -f k8s/airflow-db.yaml
	kubectl apply -f k8s/airflow-db-svc.yaml
	kubectl apply -f k8s/airflow.yaml
	kubectl apply -f k8s/airflow-svc-external.yaml

redeploy:
	kubectl rollout restart deployment/airflow
	kubectl rollout status --timeout=3m deployment/airflow

IP:=$(shell kubectl get svc airflow-svc -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
get_url:
	@echo http://${IP}/admin

