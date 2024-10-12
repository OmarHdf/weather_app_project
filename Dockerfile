# Utiliser une image de base officielle avec Python
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de votre projet dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application écoute
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python3", "app.py"]

