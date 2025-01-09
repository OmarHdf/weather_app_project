pipeline {
    agent any

    environment {
        // Variables d'environnement pour les credentials Docker
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')  // Utilisation de l'ID de credential pour Docker Hub
        SONARQUBE = 'SonarQube'  // Nom de la configuration SonarQube dans Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout du code depuis GitHub
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // Installation des dépendances et construction de l'image Docker
                script {
                    sh 'pip install -r requirements.txt'
                    sh 'docker build -t weather_app .'
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                // Exécution du scan SonarQube pour l'analyse de code
                script {
                    withSonarQubeEnv(SONARQUBE) {
                        sh 'mvn sonar:sonar -Dsonar.projectKey=weather_app_project -Dsonar.sources=.'
                    }
                }
            }
        }

        stage('Security Scan with Trivy') {
            steps {
                // Exécution du scan de sécurité avec Trivy sur l'image Docker
                script {
                    sh 'docker pull aquasec/trivy'
                    sh 'trivy image --severity HIGH,CRITICAL weather_app'
                }
            }
        }

        stage('Test') {
            steps {
                // Exécution des tests unitaires
                script {
                    sh 'pytest tests'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Push de l'image Docker sur Docker Hub
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                        sh 'docker tag weather_app $DOCKER_USERNAME/weather_app:latest'
                        sh 'docker push $DOCKER_USERNAME/weather_app:latest'
                    }
                }
            }
        }
    }

    post {
        always {
            // Nettoyage du workspace après l'exécution du pipeline
            cleanWs()
        }

        success {
            // Actions à effectuer en cas de succès
            echo 'Pipeline réussi !'
        }

        failure {
            // Actions à effectuer en cas d'échec
            echo 'Le pipeline a échoué.'
        }
    }
}


