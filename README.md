# SoftDesk Support API

## Présentation du projet

SoftDesk Support API est une API RESTful pour le suivi et la gestion de problèmes techniques dans divers projets de développement. Elle offre une interface complète permettant aux utilisateurs de créer des projets, d'ajouter des contributeurs, de signaler des problèmes, et de suivre leur résolution grâce à un système de commentaires.

Cette application a été développée avec Django et Django REST Framework, offrant une API robuste et sécurisée.

## Fonctionnalités principales

- **Gestion des utilisateurs** conforme au RGPD
- **Authentification JWT** sécurisée avec rotation des tokens
- **Gestion de projets** (création, modification, listing)
- **Système de contributeurs** pour contrôler l'accès aux projets
- **Suivi des problèmes** (issues) avec priorité, tags, et statut
- **Commentaires** sur les problèmes pour faciliter la communication
- **Système de permissions** avancé
- **Documentation API** avec Swagger et ReDoc
- **Interface CLI** pour interagir avec l'API

## Architecture technique

### Backend

- **Django 5.0** : Framework web Python
- **Django REST Framework** : Pour la création d'API RESTful
- **Simple JWT** : Pour l'authentification par tokens JWT
- **DRF Nested Routers** : Pour les routes API imbriquées
- **Swagger/OpenAPI** : Pour la documentation de l'API

### Base de données

- **SQLite** : Base de données légère incluse avec Django
- **Modèles** : 
  - `User` : Gestion des utilisateurs conforme au RGPD
  - `Project` : Projets de développement
  - `Contributor` : Lien entre utilisateurs et projets
  - `Issue` : Problèmes/tâches à résoudre
  - `Comment` : Commentaires sur les problèmes

### Interface CLI

- **Python** : Langage de programmation
- **Requests** : Pour les appels API
- **Rich** : Pour une interface console améliorée
- **JWT** : Pour la gestion des tokens d'authentification

## Installation

### Prérequis

- Python 3.8+
- Git

### Procédure d'installation

1. Cloner le dépôt :
   ```
   git clone <url-du-depot>
   cd project10
   ```

2. Exécuter le script d'installation :
   ```
   chmod +x setup_dev.sh
   ./setup_dev.sh
   ```

Ce script automatise l'ensemble de la configuration :
- Création d'un environnement virtuel Python
- Installation des dépendances
- Application des migrations de base de données
- Création d'utilisateurs de démonstration
- Configuration des outils de développement

### Utilisateurs de démonstration

Le script crée automatiquement 5 utilisateurs de test :

| Nom d'utilisateur | Mot de passe | Email                | Âge | Rôle                |
|-------------------|--------------|----------------------|-----|---------------------|
| admin             | Password123  | admin@example.com    | 30  | Admin / Superuser   |
| user1             | Password123  | user1@example.com    | 25  | Utilisateur         |
| user2             | Password123  | user2@example.com    | 28  | Utilisateur         |
| user3             | Password123  | user3@example.com    | 22  | Utilisateur         |
| user4             | Password123  | user4@example.com    | 35  | Utilisateur         |

De plus, le script crée :
- Un projet de démonstration créé par "admin"
- Une issue de démonstration assignée à "user1"
- Un commentaire de démonstration

## Démarrage du serveur

Pour lancer le serveur de développement :

```bash
source venv/bin/activate
python manage.py runserver
```

Le serveur sera accessible à l'adresse http://localhost:8000/.

## Interface CLI SoftDesk Mini

L'application inclut une interface en ligne de commande pour interagir avec l'API.

### Lancement de l'interface CLI

```bash
source venv/bin/activate
python softdesk_mini.py
```

ou

```bash
chmod +x softdesk_mini.py
./softdesk_mini.py
```

### Fonctionnalités de l'interface CLI

- **Authentification** : Connexion, inscription, déconnexion
- **Gestion des projets** : Création et listage des projets
- **Gestion des contributeurs** : Ajout et listage des contributeurs
- **Gestion des issues** : Création et listage des problèmes
- **Gestion des commentaires** : Ajout et listage des commentaires

L'interface est intuitive et propose un menu contextuel qui s'adapte selon les actions disponibles.

## Description du script setup_dev.sh

Le script `setup_dev.sh` automatise l'installation et la configuration de l'environnement de développement :

1. **Vérification de Python** : S'assure que Python 3 est installé
2. **Création d'un environnement virtuel** : Isole les dépendances du projet
3. **Activation de l'environnement virtuel** : Prépare l'environnement
4. **Installation des dépendances** : Installe les packages requis depuis requirements.txt
5. **Installation des outils de développement** : Configure Black et Flake8
6. **Vérification des migrations** : Applique les migrations à la base de données
7. **Vérification de la qualité du code** : Configure le formatage automatique
8. **Création d'utilisateurs de démonstration** : Génère des utilisateurs de test et des données de démo
9. **Option de création d'un superutilisateur** : Permet d'ajouter un superutilisateur supplémentaire

## Structure de la base de données

La base de données SQLite comprend les tables suivantes :

### Table Users
- Gestion des utilisateurs avec authentification
- Champs supplémentaires pour conformité RGPD (âge, consentements)

### Table Projects
- Projets de développement
- Types : Backend, Frontend, iOS, Android

### Table Contributors
- Relation entre utilisateurs et projets
- Définit le rôle de chaque utilisateur (Auteur ou Contributeur)

### Table Issues
- Problèmes/tâches à résoudre
- Priorités : Low, Medium, High
- Tags : Bug, Feature, Task
- Statuts : To Do, In Progress, Finished

### Table Comments
- Commentaires sur les issues
- Identifiés par UUID pour sécurité accrue

## Documentation de l'API

L'API est documentée via Swagger et ReDoc. Après avoir lancé le serveur, vous pouvez accéder à :

- **Swagger UI** : http://localhost:8000/swagger/
- **ReDoc** : http://localhost:8000/redoc/

## Permissions et sécurité

Le système de permissions comprend :

- **Authentification JWT** : Tokens d'accès et de rafraîchissement
- **Permissions par projet** : Seuls les contributeurs d'un projet peuvent y accéder
- **Permissions par ressource** : Restrictions selon le rôle de l'utilisateur
- **Protection des données** : Conformité RGPD pour les informations utilisateur

## Exemple d'utilisation du CLI

1. **Connexion** :
   - Sélectionnez "Se connecter"
   - Entrez "admin" et "Password123"

2. **Créer un projet** :
   - Sélectionnez "Créer un projet"
   - Complétez les informations demandées

3. **Ajouter un contributeur** :
   - Sélectionnez le projet
   - Choisissez "Ajouter un contributeur"
   - Entrez l'ID de l'utilisateur

4. **Créer une issue** :
   - Dans un projet, sélectionnez "Créer une issue"
   - Remplissez les informations requises

5. **Ajouter un commentaire** :
   - Sélectionnez une issue
   - Choisissez "Ajouter un commentaire"
   - Entrez votre commentaire

## Contribution au projet

Pour maintenir la qualité du code, le projet utilise :

- **Black** : Pour le formatage automatique du code
- **Flake8** : Pour l'analyse statique et le respect des conventions PEP 8
- **Git** : Pour le contrôle de version

## Licence

Ce projet est distribué sous licence libre.

---

*Développé dans le cadre du projet 10 d'OpenClassrooms pour la formation Développeur d'application Python* 