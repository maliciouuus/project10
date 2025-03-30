#!/bin/bash

# Création d'un fichier d'environnement Postman pour l'API SoftDesk
# Cela facilitera l'importation de l'environnement dans Postman

TIMESTAMP=$(date +%s)
ENV_FILE="softdesk_api_environment.json"

cat > "$ENV_FILE" << EOF
{
	"id": "$(uuidgen || echo "d5cad8e1-2f6c-4e99-9a17-b5c2d3e8f3c5")",
	"name": "SoftDesk API Environment",
	"values": [
		{
			"key": "base_url",
			"value": "http://localhost:6060",
			"type": "default",
			"enabled": true
		},
		{
			"key": "timestamp",
			"value": "$TIMESTAMP",
			"type": "default",
			"enabled": true
		},
		{
			"key": "username",
			"value": "testuser_$TIMESTAMP",
			"type": "default",
			"enabled": true
		},
		{
			"key": "email",
			"value": "test_$TIMESTAMP@example.com",
			"type": "default",
			"enabled": true
		},
		{
			"key": "token",
			"value": "",
			"type": "default",
			"enabled": true
		},
		{
			"key": "refresh_token",
			"value": "",
			"type": "default",
			"enabled": true
		},
		{
			"key": "user_id",
			"value": "",
			"type": "default",
			"enabled": true
		},
		{
			"key": "project_id",
			"value": "",
			"type": "default",
			"enabled": true
		},
		{
			"key": "issue_id",
			"value": "",
			"type": "default",
			"enabled": true
		},
		{
			"key": "comment_id",
			"value": "",
			"type": "default",
			"enabled": true
		}
	],
	"_postman_variable_scope": "environment",
	"_postman_exported_at": "$(date -Iseconds)",
	"_postman_exported_using": "Postman/10.13.5"
}
EOF

echo "L'environnement Postman a été généré dans le fichier: $ENV_FILE"
echo "Importez ce fichier dans Postman pour configurer votre environnement de test." 