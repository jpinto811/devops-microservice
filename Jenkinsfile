pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
        API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
        SECRET_KEY = "ju3W7bNrqh0Nj8GJoP518wCR7fkIld6ygVKuQaBy4C1AIIOFm7WbgAE1lIyDWyXq2t/JisHNwWMro+qBEDsMbA=="
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
                        echo "⚠️ Port 8000 is already in use. Stopping and removing any running container..."
                        docker stop test-microservice || true
                        docker rm -f test-microservice || true
                    fi
                '''

                echo '🧪 Starting microservice container for testing...'
                sh '''
                    docker rm -f test-microservice || true
                    docker run -d --name test-microservice -p 8000:8000 \
                        -e API_KEY=$API_KEY -e SECRET_KEY=$SECRET_KEY $DOCKER_IMAGE
                    sleep 5
                    docker logs test-microservice
                '''

                echo '🔎 Running tests inside Docker container...'
                sh '''
                    docker run --rm --network=host \
                        -e API_KEY=$API_KEY -e SECRET_KEY=$SECRET_KEY \
                        -e PYTHONPATH=/app \
                        $DOCKER_IMAGE pytest tests/ --maxfail=1 --disable-warnings -v
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up test container...'
            sh '''
                docker stop test-microservice || true
                docker rm -f test-microservice || true
            '''
        }
        success {
            echo '✅ Build and Test Passed! 🎉'
        }
        failure {
            echo '❌ Build or Test Failed. Check logs. 🔥'
        }
    }
}
