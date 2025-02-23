pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git 'https://github.com/jpinto811/devops-microservice.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Test') {
            steps {
                echo 'Setting up virtual environment and running tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    pytest tests/
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo 'Logging into Docker Hub...'
                withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login -u mtobias13 --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl rollout status deployment my-microservice'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for errors.'
        }
    }
}
