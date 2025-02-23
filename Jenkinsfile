pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/jpinto811/devops-microservice.git'
        BRANCH = 'main'
        IMAGE_NAME = 'my-microservice'
        K8S_DIR = 'k8s/'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                pip install -r requirements.txt
                pytest tests/
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                sh '''
                docker tag ${IMAGE_NAME} mydockerhub/${IMAGE_NAME}:latest
                docker push mydockerhub/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh '''
                kubectl apply -f ${K8S_DIR}
                kubectl rollout status deployment/my-microservice
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}

