#!/bin/bash

# Script de configuration de l'environnement de développement pour SoftDesk API
# Auteur: Sacha

# Couleurs pour améliorer la lisibilité des messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration du port
API_PORT=8000

echo -e "${BLUE}=== Configuration de l'environnement de développement SoftDesk API ===${NC}"

# 1. Vérification de Python
echo -e "\n${YELLOW}1. Vérification de l'installation Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 n'est pas installé. Veuillez l'installer avant de continuer.${NC}"
    exit 1
fi
python_version=$(python3 --version)
echo -e "${GREEN}$python_version détecté.${NC}"

# 2. Création de l'environnement virtuel
echo -e "\n${YELLOW}2. Création d'un environnement virtuel...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Environnement virtuel créé avec succès.${NC}"
else
    echo -e "${GREEN}L'environnement virtuel existe déjà.${NC}"
fi

# 3. Activation de l'environnement virtuel
echo -e "\n${YELLOW}3. Activation de l'environnement virtuel...${NC}"
source venv/bin/activate || { echo -e "${RED}L'activation de l'environnement virtuel a échoué.${NC}"; exit 1; }
echo -e "${GREEN}Environnement virtuel activé.${NC}"

# 4. Installation des dépendances
echo -e "\n${YELLOW}4. Installation des dépendances...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || { echo -e "${RED}Installation des dépendances échouée.${NC}"; exit 1; }
    echo -e "${GREEN}Dépendances installées avec succès.${NC}"
else
    echo -e "${RED}Le fichier requirements.txt est introuvable.${NC}"
    exit 1
fi

# 5. Installation des outils de développement
echo -e "\n${YELLOW}5. Installation des outils de développement...${NC}"
pip install black flake8 flake8-html || { echo -e "${RED}Installation des outils de développement échouée.${NC}"; exit 1; }
echo -e "${GREEN}Outils de développement installés avec succès.${NC}"

# 6. Vérification des migrations
echo -e "\n${YELLOW}6. Vérification des migrations...${NC}"
python manage.py makemigrations
python manage.py migrate || { echo -e "${RED}Application des migrations échouée.${NC}"; exit 1; }
echo -e "${GREEN}Migrations appliquées avec succès.${NC}"

# 7. Vérification de la qualité du code avec génération de rapport HTML
echo -e "\n${YELLOW}7. Vérification de la qualité du code avec Flake8...${NC}"
# Formatage du code avec Black
echo -e "${BLUE}Formatage du code avec Black...${NC}"
black --line-length 79 users projects softdesk
# Génération du rapport HTML avec Flake8
echo -e "${BLUE}Génération du rapport de qualité du code avec Flake8...${NC}"
mkdir -p flake8_report
flake8 --format=html --htmldir=flake8_report users projects softdesk
echo -e "${GREEN}Rapport de qualité du code généré dans le dossier 'flake8_report'.${NC}"

# 8. Création de la base de données de démo avec 5 utilisateurs
echo -e "\n${YELLOW}8. Création d'utilisateurs de démonstration...${NC}"
if [ -f "create_demo_users.py" ]; then
    python create_demo_users.py
    echo -e "${GREEN}Utilisateurs de démonstration créés avec succès.${NC}"
else
    echo -e "${RED}Le fichier create_demo_users.py est introuvable.${NC}"
    echo -e "${YELLOW}Veuillez vous assurer que le fichier create_demo_users.py existe pour générer les données de démo.${NC}"
    exit 1
fi

# 9. Création d'un superutilisateur (optionnel)
echo -e "\n${YELLOW}9. Voulez-vous créer un superutilisateur supplémentaire? (o/N)${NC}"
read -r create_superuser
if [[ "$create_superuser" =~ ^[Oo]$ ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}Superutilisateur créé avec succès.${NC}"
else
    echo -e "${BLUE}Création du superutilisateur ignorée.${NC}"
fi

# 10. Instructions finales
echo -e "\n${GREEN}=== Configuration terminée avec succès! ===${NC}"
echo -e "\nPour lancer le serveur de développement, exécutez:"
echo -e "${BLUE}    source venv/bin/activate${NC}"
echo -e "${BLUE}    python manage.py runserver ${API_PORT}${NC}"
echo -e "\nPour générer un nouveau rapport de qualité du code, exécutez:"
echo -e "${BLUE}    flake8 --format=html --htmldir=flake8_report users projects softdesk${NC}"
echo -e "\nPour tester l'API, utilisez:"
echo -e "${BLUE}    ./softdesk_mini.py${NC}"
echo -e "\nPour accéder à la documentation API, connectez-vous d'abord puis accédez à:"
echo -e "${BLUE}    http://localhost:${API_PORT}/swagger/${NC}"
echo -e "${BLUE}    http://localhost:${API_PORT}/redoc/${NC}"
echo -e "\nPour consulter le rapport de qualité du code:"
echo -e "${BLUE}    Ouvrez le fichier flake8_report/index.html dans votre navigateur${NC}"

echo -e "\nUtilisateurs de démonstration créés:"
echo -e "${YELLOW}    Username: admin    | Password: Password123${NC}"
echo -e "${YELLOW}    Username: user1    | Password: Password123${NC}"
echo -e "${YELLOW}    Username: user2    | Password: Password123${NC}"
echo -e "${YELLOW}    Username: user3    | Password: Password123${NC}"
echo -e "${YELLOW}    Username: user4    | Password: Password123${NC}" 