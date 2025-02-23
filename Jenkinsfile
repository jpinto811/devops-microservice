pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest tests/'
            }
        }
    }

    post {
        success {
            echo '✅ Build and Test Passed!'
        }
        failure {
            echo '❌ Build or Test Failed. Check logs.'
        }
    }
}
