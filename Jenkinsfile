pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python...'
                sh 'python -m venv venv'
                sh '. venv/bin/activate'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh './Frontend/Website/test_app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // sh './Deployment/deployment.sh.sh'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'deactivate'
            sh 'rm -rf venv'
        }

        success {
            echo 'Build succeeded!'
        }

        failure {
            echo 'Build failed!'
        }
    }
}
