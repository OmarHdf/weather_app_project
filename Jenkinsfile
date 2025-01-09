Voici un exemple de **Jenkinsfile** que vous pouvez ajouter à votre projet pour mettre en place un pipeline DevSecOps. Ce pipeline inclut des étapes pour l'analyse de sécurité, les tests unitaires et le déploiement.

### **1. Créer le fichier Jenkinsfile**
Dans votre projet, créez un fichier nommé `Jenkinsfile` :

```bash
touch Jenkinsfile
```

Ensuite, éditez le fichier avec votre éditeur préféré :

```bash
nano Jenkinsfile
```

---

### **2. Exemple de contenu pour le Jenkinsfile**

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather_app"
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials') // Configurer dans Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère le code du dépôt Git
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installe les dépendances nécessaires
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Static Code Analysis') {
            steps {
                // Analyse le code avec des outils comme Bandit
                sh 'bandit -r .'
            }
        }

        stage('Unit Tests') {
            steps {
                // Exécute les tests unitaires
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Construire l'image Docker
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Security Scanning') {
            steps {
                // Analyse de sécurité avec Trivy
                sh 'trivy image $IMAGE_NAME'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Pousser l'image sur Docker Hub
                sh """
                docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW
                docker tag $IMAGE_NAME $DOCKER_CREDENTIALS_USR/$IMAGE_NAME:latest
                docker push $DOCKER_CREDENTIALS_USR/$IMAGE_NAME:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                // Déployer l'application
                sh 'docker run -d -p 5000:5000 $IMAGE_NAME'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé'
        }
        success {
            echo 'Pipeline réussi !'
        }
        failure {
            echo 'Pipeline échoué.'
        }
   
}
}
