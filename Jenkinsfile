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
                echo 'Starting docker-compose...'
                sh "docker-compose build"
                sh "docker-compose up -d"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh "docker-compose exec -T backend pytest"
            }
        }
        stage('Linters') {
            steps {
                echo 'Linters...'
                sh "docker-compose exec -T backend pylint --rcfile=.pylintrc ./"
            }
        }
    }
    post {
       always {
            sh 'docker logout'
          }
    }
}