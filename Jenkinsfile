     pipeline {
    agent any

    environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building images...'
                sh "docker build -f ./backend/build/Dockerfile -t mirrss/fastapi_template:latest ."
                echo 'Pushing images...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh "docker push mirrss/fastapi_template:latest"
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh "minikube start"
                sh "kubectl apply -f ."
            }
        }
    }
    post {
       always {
            sh 'docker logout'
          }
    }
}