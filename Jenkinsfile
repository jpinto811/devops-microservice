pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
        GIT_REPO = 'https://github.com/jpinto811/devops-microservice.git'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: GIT_REPO]]])
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
                    pip install --no-cache-dir --break-system-packages -r requirements.txt
                    pytest tests/ --maxfail=1 --disable-warnings
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo 'Logging into Docker Hub...'
                withCredentials([string(credentialsId: 'DOCKER_PASSWORD', variable: 'DOCKER_PASSWORD')]) {
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
                    if [ -d "k8s" ]; then
                        kubectl apply -f k8s/deployment.yaml
                        kubectl rollout status deployment my-microservice
                    else
                        echo "⚠️ Directory k8s/ not found. Skipping deployment."
                    fi
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
