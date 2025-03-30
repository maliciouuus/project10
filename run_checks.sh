#!/bin/bash

# Script pour vérifier la qualité du code et exécuter les tests
# Auteur: Sacha

# Couleurs pour améliorer la lisibilité des messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paramètres par défaut
RUN_FORMAT=true
RUN_UNIT_TESTS=true
RUN_API_TESTS=true
RUN_POSTMAN_TESTS=false  # Désactivé par défaut car nécessite newman

# Fonction d'affichage d'aide
show_help() {
    echo -e "${BLUE}Usage: $0 [options]${NC}"
    echo -e "Options:"
    echo -e "  -h, --help           Affiche cette aide"
    echo -e "  --no-format          Ne pas formater le code"
    echo -e "  --no-unit            Ne pas exécuter les tests unitaires"
    echo -e "  --no-api             Ne pas exécuter les tests API"
    echo -e "  --with-postman       Exécuter les tests Postman (nécessite newman)"
    echo -e "  --all                Exécuter tous les tests (y compris Postman)"
    echo
}

# Traitement des arguments
for arg in "$@"
do
    case $arg in
        -h|--help)
            show_help
            exit 0
            ;;
        --no-format)
            RUN_FORMAT=false
            shift
            ;;
        --no-unit)
            RUN_UNIT_TESTS=false
            shift
            ;;
        --no-api)
            RUN_API_TESTS=false
            shift
            ;;
        --with-postman)
            RUN_POSTMAN_TESTS=true
            shift
            ;;
        --all)
            RUN_FORMAT=true
            RUN_UNIT_TESTS=true
            RUN_API_TESTS=true
            RUN_POSTMAN_TESTS=true
            shift
            ;;
        *)
            # Ignorer l'argument inconnu
            shift
            ;;
    esac
done

echo -e "${YELLOW}=== Vérification de la qualité du code et tests ===${NC}"

# 1. Formater le code avec Black et vérifier avec Flake8
if [ "$RUN_FORMAT" = true ]; then
    echo -e "\n${YELLOW}1. Formatage et vérification du code${NC}"
    ./format_code.sh
else
    echo -e "\n${YELLOW}1. Formatage et vérification du code (ignoré)${NC}"
fi

# 2. Exécuter les tests unitaires
if [ "$RUN_UNIT_TESTS" = true ]; then
    echo -e "\n${YELLOW}2. Exécution des tests unitaires${NC}"
    python manage.py test
else
    echo -e "\n${YELLOW}2. Exécution des tests unitaires (ignoré)${NC}"
fi

# 3. Exécuter les tests d'API
if [ "$RUN_API_TESTS" = true ]; then
    echo -e "\n${YELLOW}3. Exécution des tests d'API${NC}"
    if [[ -f "./test_api_complete.sh" ]]; then
        echo -e "${GREEN}Exécution du script de test d'API...${NC}"
        ./test_api_complete.sh
    else
        echo -e "${RED}Script de test d'API non trouvé.${NC}"
    fi
else
    echo -e "\n${YELLOW}3. Exécution des tests d'API (ignoré)${NC}"
fi

# 4. Exécuter les tests Postman
if [ "$RUN_POSTMAN_TESTS" = true ]; then
    echo -e "\n${YELLOW}4. Exécution des tests Postman${NC}"
    
    # Vérifier si newman est installé
    if ! command -v newman &> /dev/null; then
        echo -e "${RED}Newman n'est pas installé. Installation en cours...${NC}"
        npm install -g newman || {
            echo -e "${RED}L'installation de Newman a échoué. Assurez-vous que npm est installé.${NC}"
            echo -e "${RED}Les tests Postman ne seront pas exécutés.${NC}"
            RUN_POSTMAN_TESTS=false
        }
    fi
    
    if [ "$RUN_POSTMAN_TESTS" = true ]; then
        if [[ -f "./softdesk_postman_collection.json" ]]; then
            # Générer l'environnement Postman si nécessaire
            if [[ -f "./create_postman_environment.sh" ]]; then
                echo -e "${GREEN}Génération de l'environnement Postman...${NC}"
                ./create_postman_environment.sh
            fi
            
            # Exécuter les tests Postman
            if [[ -f "./softdesk_api_environment.json" ]]; then
                echo -e "${GREEN}Exécution des tests Postman...${NC}"
                newman run softdesk_postman_collection.json -e softdesk_api_environment.json
            else
                echo -e "${YELLOW}Exécution des tests Postman sans environnement...${NC}"
                newman run softdesk_postman_collection.json
            fi
        else
            echo -e "${RED}Collection Postman non trouvée.${NC}"
        fi
    fi
else
    echo -e "\n${YELLOW}4. Exécution des tests Postman (ignoré)${NC}"
fi

echo -e "\n${GREEN}Terminé !${NC}" 