#!/bin/bash

# Script de nettoyage du projet avant de pousser
# Auteur: Claude

# Couleurs pour améliorer la lisibilité des messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Nettoyage du projet SoftDesk Support API avant push ===${NC}"

# 1. Suppression de tous les __pycache__ et fichiers .pyc
echo -e "\n${YELLOW}1. Suppression des fichiers cache Python...(toujours recommandé)${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
echo -e "${GREEN}Fichiers cache Python supprimés.${NC}"

# 2. Suppression des fichiers temporaires
echo -e "\n${YELLOW}2. Suppression des fichiers temporaires...(toujours recommandé)${NC}"
find . -name "*.swp" -delete
find . -name "*~" -delete
find . -name "*.bak" -delete
find . -name "*.tmp" -delete
find . -name "*.orig" -delete
echo -e "${GREEN}Fichiers temporaires supprimés.${NC}"

# 3. Option pour supprimer la base de données
echo -e "\n${YELLOW}3. Voulez-vous supprimer la base de données? (uniquement si vous ne souhaitez pas partager les données de démonstration) (o/N)${NC}"
read -r delete_db
if [[ "$delete_db" =~ ^[Oo]$ ]]; then
    rm -f db.sqlite3*
    echo -e "${GREEN}Base de données supprimée.${NC}"
else
    echo -e "${BLUE}Base de données conservée.${NC}"
fi

# 4. Option pour supprimer les scripts de développement
echo -e "\n${YELLOW}4. Voulez-vous supprimer le script create_demo_users.py s'il existe? (o/N)${NC}"
read -r delete_demo_script
if [[ "$delete_demo_script" =~ ^[Oo]$ ]]; then
    if [ -f "create_demo_users.py" ]; then
        rm -f create_demo_users.py
        echo -e "${GREEN}Script create_demo_users.py supprimé.${NC}"
    else
        echo -e "${BLUE}Le script create_demo_users.py n'existe pas.${NC}"
    fi
else
    echo -e "${BLUE}Script create_demo_users.py conservé.${NC}"
fi

# 5. Option pour supprimer les fichiers de configuration de l'IDE
echo -e "\n${YELLOW}5. Voulez-vous supprimer les fichiers de configuration d'IDE (.vscode, .idea)? (o/N)${NC}"
read -r delete_ide_configs
if [[ "$delete_ide_configs" =~ ^[Oo]$ ]]; then
    rm -rf .vscode .idea
    echo -e "${GREEN}Fichiers de configuration d'IDE supprimés.${NC}"
else
    echo -e "${BLUE}Fichiers de configuration d'IDE conservés.${NC}"
fi

echo -e "\n${GREEN}=== Nettoyage terminé ! ===${NC}"
echo -e "Votre projet est maintenant prêt à être poussé vers un dépôt Git."
echo -e "Commandes Git recommandées:"
echo -e "${BLUE}    git add .${NC}"
echo -e "${BLUE}    git commit -m \"Version finale du projet SoftDesk Support API\"${NC}"
echo -e "${BLUE}    git push${NC}" 