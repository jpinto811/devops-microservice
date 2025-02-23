pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
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
                echo '🧪 Running tests inside Docker container...'
                sh '''
                    docker run --rm -e PYTHONPATH=/app $DOCKER_IMAGE pytest tests/ --maxfail=1 --disable-warnings -v
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build and Test Passed! 🎉'
        }
        failure {
            echo '❌ Build or Test Failed. Check logs. 🔥'
        }
    }
}
