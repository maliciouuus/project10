# Collection Postman pour l'API SoftDesk

Cette collection Postman a été créée pour tester l'API SoftDesk de manière complète. Elle reproduit la logique du script `test_api_complete.sh` mais dans un environnement Postman plus visuel et interactif.

## Prérequis

- [Postman](https://www.postman.com/downloads/) installé sur votre machine
- L'API SoftDesk en cours d'exécution (par défaut sur `http://localhost:6060`)

## Installation et configuration

1. Importez le fichier `softdesk_api_test_collection.json` dans Postman
2. Créez un environnement Postman pour stocker les variables nécessaires
3. Configurez l'environnement avec la variable `base_url` pointant vers votre API (par défaut : `http://localhost:6060`)

## Structure de la collection

La collection est organisée en 5 sections principales, qui doivent être exécutées dans l'ordre :

1. **Tests d'authentification et autorisations**
   - Test d'accès sans token
   - Création d'utilisateur
   - Test de validation des contraintes (âge minimum)
   - Connexion et obtention de token
   - Rafraîchissement de token

2. **Tests des projets**
   - Création de projet
   - Liste des projets
   - Test d'accès avec authentification

3. **Tests des issues**
   - Création d'issue
   - Modification d'issue
   - Liste des issues
   - Détail d'une issue

4. **Tests des commentaires**
   - Création de commentaire
   - Liste des commentaires
   - Détail d'un commentaire

5. **Tests de suppression**
   - Suppression de commentaire
   - Suppression d'issue
   - Suppression de projet

## Fonctionnalités clés

- **Gestion des variables d'environnement** : Tous les identifiants (user_id, project_id, issue_id, comment_id) sont automatiquement extraits des réponses API et stockés pour les requêtes suivantes.
- **Scripts de pré-requête** : Vérifie que les IDs nécessaires sont disponibles avant d'exécuter une requête.
- **Tests automatisés** : Chaque requête inclut des tests pour vérifier la validité de la réponse.
- **Gestion des erreurs** : Des messages d'erreur détaillés en cas d'échec.
- **Logging** : Des messages console pour suivre l'exécution des tests.

## Utilisation

### Exécution manuelle

1. Ouvrez Postman et sélectionnez l'environnement créé
2. Parcourez la collection et exécutez les requêtes une par une dans l'ordre

### Exécution automatisée (Runner)

1. Cliquez sur le bouton "Runner" dans Postman
2. Sélectionnez la collection SoftDesk API
3. Configurez les options d'exécution (delay entre requêtes, etc.)
4. Lancez l'exécution

## Points importants

1. **Ordre d'exécution** : Les tests sont conçus pour être exécutés dans un ordre spécifique, car ils dépendent les uns des autres.
2. **Variables d'environnement** : Les variables comme `token`, `project_id`, `issue_id`, et `comment_id` sont essentielles au bon fonctionnement des tests.
3. **Scripts de pré-requête** : Ils vérifient que toutes les dépendances sont satisfaites avant d'exécuter la requête.

## Dépannage

- **Erreurs 401 (Unauthorized)** : Vérifiez que le token est correctement stocké et transmis.
- **Erreurs 404 (Not Found)** : Vérifiez que les IDs (projet, issue, commentaire) sont correctement sauvegardés.
- **Erreurs 400 (Bad Request)** : Vérifiez le format des données envoyées.

Si les problèmes persistent, consultez les logs dans la console Postman pour plus de détails.

## Avantages par rapport au script Bash

- Interface graphique interactive
- Visualisation facile des résultats
- Historique des réponses
- Possibilité de modifier et rejouer facilement les requêtes
- Meilleure gestion des erreurs avec retour visuel
- Possibilité d'exporter les résultats des tests 