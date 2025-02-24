pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
        KUBECONFIG_CRED = 'kubeconfig'  // ID de la credencial en Jenkins
    }

    stages {
        stage('Build') {
            steps {
                echo '🚀 Building Docker image...'
                sh '''
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🛑 Checking if port 8000 is already in use...'
                sh '''
                    if [ "$(docker ps -q -f publish=8000)" ]; then
                        echo "⚠️ Port 8000 is already in use. Stopping any running container..."
                        docker stop $(docker ps -q -f publish=8000) || true
                    fi
                '''

                echo '🧪 Starting microservice container for testing...'
                sh '''
                    docker run -d --name test-microservice -p 8000:8000 $DOCKER_IMAGE
                    sleep 5  # Esperar a que el servicio se levante
                    docker logs test-microservice  # Verifica si el servicio arrancó
                '''

                echo '🔎 Running tests inside Docker container...'
                sh '''
                    docker run --rm --network=host -e PYTHONPATH=/app $DOCKER_IMAGE pytest tests/ --maxfail=1 --disable-warnings -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: env.KUBECONFIG_CRED, variable: 'KUBECONFIG')]) {
                        echo '🚀 Deploying to Kubernetes...'
                        sh '''
                            export KUBECONFIG=$KUBECONFIG
                            kubectl apply -f k8s/
                            kubectl rollout status deployment my-microservice
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up test container...'
            sh '''
                docker stop test-microservice || true
                docker rm test-microservice || true
            '''
        }
        success {
            echo '✅ Build, Test, and Deploy Completed Successfully! 🎉'
        }
        failure {
            echo '❌ Build, Test, or Deploy Failed. Check logs. 🔥'
        }
    }
}
