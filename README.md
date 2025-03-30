# SoftDesk Support API

Une API RESTful pour la gestion de projets et le suivi des problèmes, développée avec Django REST Framework.

## Fonctionnalités

- Authentification JWT
- Gestion des utilisateurs conforme au RGPD
- Gestion des projets et des contributeurs
- Suivi des problèmes (issues) et des commentaires
- Pagination des résultats
- Sécurité et permissions avancées

## Installation

### Installation standard

1. Cloner le dépôt :
```bash
git clone <repository_url>
cd softdesk
```

2. Utiliser le script d'installation automatique :
```bash
./setup_dev.sh
```

Ou procéder manuellement :

1. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Appliquer les migrations :
```bash
python manage.py migrate
```

4. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

5. Lancer le serveur de développement :
```bash
python manage.py runserver 6060
```

## Contrôle de qualité du code

Ce projet utilise plusieurs outils pour assurer la qualité et la cohérence du code :

- **Black** : Formateur de code automatique
- **Flake8** : Linter pour vérifier la conformité au style PEP 8

### Scripts de vérification

Plusieurs scripts sont disponibles pour faciliter le développement :

- `format_code.sh` : Formate le code avec Black et vérifie avec Flake8
- `run_checks.sh` : Exécute le formatage, les tests unitaires et les tests d'API

```bash
# Pour formater le code
./format_code.sh

# Pour exécuter tous les tests
./run_checks.sh

# Pour voir toutes les options disponibles
./run_checks.sh --help
```

Pour plus de détails sur nos conventions de style, consultez [le guide de style](docs/STYLE_GUIDE.md).

## Tests automatisés

Cette API comprend un ensemble de tests qui peuvent être exécutés via Postman ou via notre runner de tests automatisé en bash.

### Utilisation des scripts de test automatisés

1. Script de test API complet :
```bash
./test_api_complete.sh
```

Ce script :
- Vérifie que l'API est accessible
- Exécute les tests dans le bon ordre
- Génère et gère automatiquement les IDs entre les requêtes

### Tests Postman

1. Générer l'environnement Postman :
```bash
./create_postman_environment.sh
```

2. Importer dans Postman :
   - La collection : `softdesk_postman_collection.json`
   - L'environnement : `softdesk_api_environment.json`

### Déboguer les tests

Si certains tests échouent, vérifiez :
1. Que le serveur Django est en cours d'exécution
2. Que tous les modèles et routes sont correctement configurés
3. Les journaux pour identifier les erreurs spécifiques

Vous pouvez également exécuter les tests avec plus de verbosité :
```bash
./run_checks.sh --all
```

## Points de terminaison de l'API

### Authentification
- POST `/api/token/` - Obtenir un token JWT
- POST `/api/token/refresh/` - Rafraîchir un token JWT

### Utilisateurs
- GET/POST `/api/users/` - Liste/Création des utilisateurs
- GET/PUT/DELETE `/api/users/{id}/` - Détails/Modification/Suppression d'un utilisateur

### Projets
- GET/POST `/api/projects/` - Liste/Création des projets
- GET/PUT/DELETE `/api/projects/{id}/` - Détails/Modification/Suppression d'un projet

### Contributeurs
- GET/POST `/api/projects/{project_id}/contributors/` - Liste/Ajout des contributeurs
- DELETE `/api/projects/{project_id}/contributors/{id}/` - Suppression d'un contributeur

### Issues
- GET/POST `/api/projects/{project_id}/issues/` - Liste/Création des issues
- GET/PUT/DELETE `/api/projects/{project_id}/issues/{id}/` - Détails/Modification/Suppression d'une issue

### Commentaires
- GET/POST `/api/projects/{project_id}/issues/{issue_id}/comments/` - Liste/Création des commentaires
- GET/PUT/DELETE `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Détails/Modification/Suppression d'un commentaire

## Sécurité

- Authentification requise pour tous les points de terminaison
- Vérification de l'âge (minimum 15 ans)
- Respect du RGPD (consentement, droit à l'oubli)
- Permissions basées sur les rôles (auteur, contributeur)
- Protection contre les vulnérabilités web courantes

## Pagination

L'API utilise la pagination par défaut avec 10 éléments par page. Utilisez les paramètres `page` et `page_size` pour naviguer dans les résultats :

```
GET /api/projects/?page=2&page_size=20
```

## Documentation

- Interface d'administration: Accessible via `/admin/` (nécessite une connexion)
- Code Style: Voir [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md) 