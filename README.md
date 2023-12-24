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
