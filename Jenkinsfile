pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'tarun08-code/taskmanager'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Code checked out from GitHub"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                sh 'docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest'
                echo "Docker image built"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                sh 'docker push ${DOCKER_IMAGE}:latest'
                echo "Image pushed to Docker Hub"
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s-deployment.yaml'
                sh 'kubectl rollout status deployment/taskmanager'
                echo "Deployed to Kubernetes"
            }
        }
        
        stage('Cleanup') {
            steps {
                sh 'docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true'
                sh 'docker system prune -f || true'
                echo "Cleanup done - disk space saved"
            }
        }
    }
    
    post {
        success {
            echo "Pipeline SUCCESS! Build ${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline FAILED! Check logs"
        }
    }
}