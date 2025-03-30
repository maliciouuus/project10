#!/bin/bash

# Script de configuration de l'environnement de développement pour SoftDesk API
# Auteur: Sacha

# Couleurs pour améliorer la lisibilité des messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
pip install black flake8 || { echo -e "${RED}Installation des outils de développement échouée.${NC}"; exit 1; }
echo -e "${GREEN}Outils de développement installés avec succès.${NC}"

# 6. Vérification des migrations
echo -e "\n${YELLOW}6. Vérification des migrations...${NC}"
python manage.py makemigrations
python manage.py migrate || { echo -e "${RED}Application des migrations échouée.${NC}"; exit 1; }
echo -e "${GREEN}Migrations appliquées avec succès.${NC}"

# 7. Vérification de la qualité du code (seulement si le script existe)
echo -e "\n${YELLOW}7. Vérification de la qualité du code...${NC}"
if [ -f "./format_code.sh" ]; then
    chmod +x ./format_code.sh
    ./format_code.sh
else
    echo -e "${YELLOW}Le script format_code.sh n'existe pas encore. Étape ignorée.${NC}"
    
    # Créer un script format_code.sh minimal
    echo -e "${BLUE}Création d'un script format_code.sh minimal...${NC}"
    cat > format_code.sh << 'EOF'
#!/bin/bash
# Script minimal pour formater le code avec Black et vérifier avec Flake8
echo "Formatage du code avec Black..."
black --line-length 79 users projects softdesk
echo "Vérification avec Flake8..."
flake8 users projects softdesk
EOF
    chmod +x format_code.sh
    echo -e "${GREEN}Script format_code.sh créé.${NC}"
fi

# 8. Création d'un superutilisateur (optionnel)
echo -e "\n${YELLOW}8. Voulez-vous créer un superutilisateur? (o/N)${NC}"
read -r create_superuser
if [[ "$create_superuser" =~ ^[Oo]$ ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}Superutilisateur créé avec succès.${NC}"
else
    echo -e "${BLUE}Création du superutilisateur ignorée.${NC}"
fi

# 9. Instructions finales
echo -e "\n${GREEN}=== Configuration terminée avec succès! ===${NC}"
echo -e "\nPour lancer le serveur de développement, exécutez:"
echo -e "${BLUE}    source venv/bin/activate${NC}"
echo -e "${BLUE}    python manage.py runserver 6060${NC}"
echo -e "\nPour exécuter les tests, utilisez:"
echo -e "${BLUE}    ./run_checks.sh${NC}"
echo -e "\nPour accéder à la documentation API, connectez-vous d'abord puis accédez à:"
echo -e "${BLUE}    http://localhost:6060/admin/${NC}" 