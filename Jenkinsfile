pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
        GITHUB_CREDENTIALS = 'github-credentials'
        REPO_URL = 'https://github.com/jpinto811/devops-microservice.git'
        WORKDIR = 'devops-microservice'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                deleteDir() // Limpiar el workspace antes de clonar
                git credentialsId: "${GITHUB_CREDENTIALS}", url: "${REPO_URL}", branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t $DOCKER_IMAGE .
                '''
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
                withCredentials([string(credentialsId: "${DOCKER_CREDENTIALS}", variable: 'DOCKER_PASSWORD')]) {
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
                sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl rollout status deployment my-microservice
                '''
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
