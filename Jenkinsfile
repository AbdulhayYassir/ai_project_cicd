pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AbdulhayYassir/ai_project_cicd.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -f Dockerfile.gui -t my-gui-app:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
}
