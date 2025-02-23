pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "mtobias13/my-microservice:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/jpinto811/devops-microservice.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate  # Corrección aquí para sh
                    pip install --no-cache-dir -r requirements.txt --break-system-packages
                    pytest tests/
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo 'Logging into Docker Hub...'
                withCredentials([string(credentialsId: 'DOCKER_PASSWORD', variable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u mtobias13 --password-stdin'
                }

                echo 'Tagging Docker image...'
                sh 'docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}'

                echo 'Pushing Docker image...'
                sh 'docker push ${DOCKER_IMAGE}'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh 'kubectl apply -f k8s/'
                sh 'kubectl rollout status deployment/my-microservice'
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
