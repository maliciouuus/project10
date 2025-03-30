#!/bin/bash

# Configuration
API_URL="http://localhost:6060"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Génération d'un identifiant unique basé sur le timestamp
TIMESTAMP=$(date +%s)
USERNAME="testuser_${TIMESTAMP}"
EMAIL="test_${TIMESTAMP}@example.com"

# Fonction pour afficher les résultats
display_result() {
    local STATUS=$1
    local EXPECTED=$2
    local DESCRIPTION=$3
    if [ "$STATUS" -eq "$EXPECTED" ]; then
        echo -e "${GREEN}✓ $DESCRIPTION - Status: $STATUS (Expected: $EXPECTED)${NC}"
    else
        echo -e "${RED}✗ $DESCRIPTION - Status: $STATUS (Expected: $EXPECTED)${NC}"
    fi
}

echo -e "${YELLOW}Test complet de l'API SoftDesk${NC}"
echo "=================================="

# 1. Tests d'authentification
echo -e "\n${YELLOW}1. Tests d'authentification et autorisations${NC}"

# 1.0 Test d'accès aux endpoints protégés sans token
echo -e "\n1.0 Tests d'accès sans authentification"

# Test projets
NO_AUTH_PROJECTS=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/projects/")
display_result $NO_AUTH_PROJECTS 401 "Accès aux projets sans token"

# Test issues
NO_AUTH_ISSUES=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/projects/1/issues/")
display_result $NO_AUTH_ISSUES 401 "Accès aux issues sans token"

# Test commentaires
NO_AUTH_COMMENTS=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/projects/1/issues/1/comments/")
display_result $NO_AUTH_COMMENTS 401 "Accès aux commentaires sans token"

# 1.1 Création d'un utilisateur (201 Created)
echo -e "\n1.1 Test de création d'utilisateur"
SIGNUP_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/auth/signup/" \
-H "Content-Type: application/json" \
-d '{
    "username": "'$USERNAME'",
    "email": "'$EMAIL'",
    "password": "TestPassword123!",
    "password2": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false
}')
STATUS=${SIGNUP_RESPONSE: -3}
display_result $STATUS 201 "Création d'utilisateur"

# 1.2 Tentative de création d'un utilisateur trop jeune (400 Bad Request)
echo -e "\n1.2 Test de création d'utilisateur trop jeune"
YOUNG_USER_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/auth/signup/" \
-H "Content-Type: application/json" \
-d '{
    "username": "younguser_'$TIMESTAMP'",
    "email": "young_'$TIMESTAMP'@example.com",
    "password": "TestPassword123!",
    "password2": "TestPassword123!",
    "age": 14,
    "can_be_contacted": false,
    "can_data_be_shared": false
}')
STATUS=${YOUNG_USER_RESPONSE: -3}
display_result $STATUS 400 "Création d'utilisateur trop jeune"

# 1.3 Connexion (200 OK)
echo -e "\n1.3 Test de connexion"
LOGIN_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/token/" \
-H "Content-Type: application/json" \
-d '{
    "username": "'$USERNAME'",
    "password": "TestPassword123!"
}')
STATUS=${LOGIN_RESPONSE: -3}
display_result $STATUS 200 "Connexion utilisateur"

# Extraction du token
TOKEN=$(echo "${LOGIN_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access', ''))")
REFRESH_TOKEN=$(echo "${LOGIN_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('refresh', ''))")

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Erreur: Impossible d'obtenir le token${NC}"
    exit 1
fi

if [ -z "$REFRESH_TOKEN" ]; then
    echo -e "${RED}Erreur: Impossible d'obtenir le refresh token${NC}"
    exit 1
fi

# 1.4 Test de rafraîchissement du token (200 OK)
echo -e "\n1.4 Test de rafraîchissement du token"
REFRESH_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/token/refresh/" \
-H "Content-Type: application/json" \
-d '{
    "refresh": "'$REFRESH_TOKEN'"
}')
STATUS=${REFRESH_RESPONSE: -3}
display_result $STATUS 200 "Rafraîchissement du token"

# Extraction du nouveau token
NEW_TOKEN=$(echo "${REFRESH_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access', ''))")

if [ -z "$NEW_TOKEN" ]; then
    echo -e "${RED}Erreur: Impossible d'obtenir le nouveau token${NC}"
else
    echo -e "${GREEN}Nouveau token obtenu: ${NEW_TOKEN:0:20}...${NC}"
    # Utiliser le nouveau token pour les requêtes suivantes
    TOKEN=$NEW_TOKEN
fi

# 1.5 Test avec le nouveau token (200 OK)
echo -e "\n1.5 Test d'accès avec le nouveau token"
TOKEN_TEST_RESPONSE=$(curl -s -w "%{http_code}" -X GET "$API_URL/api/projects/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${TOKEN_TEST_RESPONSE: -3}
display_result $STATUS 200 "Accès avec le nouveau token"

# 2. Tests des projets
echo -e "\n${YELLOW}2. Tests des projets${NC}"

# 2.1 Création d'un projet (201 Created)
echo -e "\n2.1 Test de création de projet"
PROJECT_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/projects/" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Projet Test",
    "description": "Description du projet test",
    "type": "BACKEND"
}')
STATUS=${PROJECT_RESPONSE: -3}
display_result $STATUS 201 "Création de projet"

# Extraction de l'ID du projet
PROJECT_ID=$(echo "${PROJECT_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

# 2.2 Liste des projets (200 OK)
echo -e "\n2.2 Test de liste des projets"
PROJECTS_LIST_RESPONSE=$(curl -s -w "%{http_code}" -X GET "$API_URL/api/projects/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${PROJECTS_LIST_RESPONSE: -3}
display_result $STATUS 200 "Liste des projets"

# 2.3 Tentative d'accès sans token (401 Unauthorized)
echo -e "\n2.3 Test d'accès sans authentification"
NO_AUTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_URL/api/projects/")
display_result $NO_AUTH_RESPONSE 401 "Accès sans authentification"

# 2.4 Liste des projets avec authentification (200 OK)
echo -e "\n2.4 Test de liste des projets avec authentification"
PROJECTS_LIST_RESPONSE=$(curl -s -w "%{http_code}" -X GET "$API_URL/api/projects/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${PROJECTS_LIST_RESPONSE: -3}
display_result $STATUS 200 "Liste des projets avec authentification"

# 3. Tests des issues
echo -e "\n${YELLOW}3. Tests des issues${NC}"

# 3.1 Création d'une issue (201 Created)
echo -e "\n3.1 Test de création d'issue"
ISSUE_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/projects/$PROJECT_ID/issues/" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Bug Test",
    "description": "Description du bug",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "TODO",
    "assignee": null
}')
STATUS=${ISSUE_RESPONSE: -3}
display_result $STATUS 201 "Création d'issue"

# Extraction de l'ID de l'issue
ISSUE_ID=$(echo "${ISSUE_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

# 3.2 Modification d'une issue (200 OK)
echo -e "\n3.2 Test de modification d'issue"
ISSUE_UPDATE_RESPONSE=$(curl -s -w "%{http_code}" -X PUT "$API_URL/api/projects/$PROJECT_ID/issues/$ISSUE_ID/" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Bug Test Updated",
    "description": "Description mise à jour",
    "priority": "MEDIUM",
    "tag": "BUG",
    "status": "IN_PROGRESS",
    "assignee": null
}')
STATUS=${ISSUE_UPDATE_RESPONSE: -3}
display_result $STATUS 200 "Modification d'issue"

# 4. Tests des commentaires
echo -e "\n${YELLOW}4. Tests des commentaires${NC}"

# 4.1 Création d'un commentaire (201 Created)
echo -e "\n4.1 Test de création de commentaire"
COMMENT_RESPONSE=$(curl -s -w "%{http_code}" -X POST "$API_URL/api/projects/$PROJECT_ID/issues/$ISSUE_ID/comments/" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "description": "Voici un commentaire de test"
}')
STATUS=${COMMENT_RESPONSE: -3}
display_result $STATUS 201 "Création de commentaire"

# Extraction de l'ID du commentaire
COMMENT_ID=$(echo "${COMMENT_RESPONSE:0:-3}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

# 4.2 Liste des commentaires (200 OK)
echo -e "\n4.2 Test de liste des commentaires"
COMMENTS_LIST_RESPONSE=$(curl -s -w "%{http_code}" -X GET "$API_URL/api/projects/$PROJECT_ID/issues/$ISSUE_ID/comments/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${COMMENTS_LIST_RESPONSE: -3}
display_result $STATUS 200 "Liste des commentaires"

# 5. Tests de suppression
echo -e "\n${YELLOW}5. Tests de suppression${NC}"

# 5.1 Suppression d'un commentaire (204 No Content)
echo -e "\n5.1 Test de suppression de commentaire"
DELETE_COMMENT_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$API_URL/api/projects/$PROJECT_ID/issues/$ISSUE_ID/comments/$COMMENT_ID/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${DELETE_COMMENT_RESPONSE: -3}
display_result $STATUS 204 "Suppression de commentaire"

# 5.2 Suppression d'une issue (204 No Content)
echo -e "\n5.2 Test de suppression d'issue"
DELETE_ISSUE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$API_URL/api/projects/$PROJECT_ID/issues/$ISSUE_ID/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${DELETE_ISSUE_RESPONSE: -3}
display_result $STATUS 204 "Suppression d'issue"

# 5.3 Suppression d'un projet (204 No Content)
echo -e "\n5.3 Test de suppression de projet"
DELETE_PROJECT_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$API_URL/api/projects/$PROJECT_ID/" \
-H "Authorization: Bearer $TOKEN")
STATUS=${DELETE_PROJECT_RESPONSE: -3}
display_result $STATUS 204 "Suppression de projet"

echo -e "\n${YELLOW}Tests terminés${NC}"
echo -e "${GREEN}Token d'accès: ${TOKEN:0:20}...${NC}"
echo -e "${GREEN}Refresh token: ${REFRESH_TOKEN:0:20}...${NC}" 
