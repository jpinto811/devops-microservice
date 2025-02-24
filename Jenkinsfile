pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mtobias13/my-microservice:latest'
        CONTAINER_NAME = 'test-microservice'
        TEST_PORT = '8000'
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
                echo '🧪 Starting microservice container for testing...'
                sh '''
                    docker run -d --name $CONTAINER_NAME -p $TEST_PORT:$TEST_PORT $DOCKER_IMAGE
                    sleep 5  # Give some time for the service to start
                    docker ps | grep $CONTAINER_NAME
                '''

                echo '🔍 Checking if service is up...'
                script {
                    def retries = 5
                    def service_up = false
                    for (int i = 0; i < retries; i++) {
                        def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:$TEST_PORT/docs", returnStdout: true).trim()
                        if (response == '200') {
                            service_up = true
                            break
                        }
                        echo "⏳ Service not up yet. Retrying in 3s... ($i/$retries)"
                        sleep(3)
                    }
                    if (!service_up) {
                        error('❌ Service did not start in time! Aborting tests.')
                    }
                }

                echo '🧪 Running tests inside Docker container...'
                sh '''
                    docker exec $CONTAINER_NAME pytest tests/ --maxfail=1 --disable-warnings -v
                '''

                echo '🛑 Stopping and cleaning up test container...'
                sh '''
                    docker stop $CONTAINER_NAME
                    docker rm $CONTAINER_NAME
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
            sh '''
                docker logs $CONTAINER_NAME || true
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
            '''
        }
    }
}
