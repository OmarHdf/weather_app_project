pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')  // Utilisation des credentials Docker Hub
        SONARQUBE = 'SonarQube'  // Nom de la configuration SonarQube dans Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout du code depuis GitHub
                checkout scm
            }
        }

        stage('Install Python and Pip') {
            steps {
                script {
                    // Installation de Python et pip si nécessaire
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Installation des dépendances et construction de l'image Docker
                    sh 'pip3 install -r requirements.txt'
                    sh 'docker build -t weather_app .'
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    // Exécution du scan SonarQube pour l'analyse de code
                    withSonarQubeEnv(SONARQUBE) {
                        sh 'mvn sonar:sonar -Dsonar.projectKey=weather_app_project -Dsonar.sources=.'
                    }
                }
            }
        }

        stage('Security Scan with Trivy') {
            steps {
                script {
                    // Exécution du scan de sécurité avec Trivy sur l'image Docker
                    sh 'docker pull aquasec/trivy'
                    sh 'trivy image --severity HIGH,CRITICAL weather_app'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Exécution des tests unitaires avec pytest
                    sh 'pytest tests'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push de l'image Docker sur Docker Hub avec les credentials
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


