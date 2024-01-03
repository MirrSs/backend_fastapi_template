# Overview

This template provides a minimal setup to get **Fast-API** backend with **JWT** auth, **asyncpg**, **sqlalchemy**.

# Build and run

You can run this project using **docker-compose** or **kubernetes**.

To run project using **docker-compose**, just use   

>   docker-compose up

To run project using **kubernetes**, you need **minikube** and **kubectl** installed and do following:

>   minikube start

In *build/kubernetes* directory use:

>   kubectl apply -f .

Also you need to configure your dns file to make requests to an ingress hostname.

To configure Prometheus and Grafana using Helm follow next steps:

>   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

>   helm repo update

>   helm install prometheus prometheus-community/prometheus

>   kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext

>   minikube service prometheus-server-ext

>   helm repo add grafana https://grafana.github.io helm-charts 

>   helm repo update

>   helm install grafana grafana/grafana

>   kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext

>   minikube service grafana-ext

To get Grafana password use: 
>   kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo