#!/usr/bin/env python3
"""Script pour créer des utilisateurs de démonstration."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "softdesk.settings")
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Project, Contributor, Issue, Comment

User = get_user_model()

# Création des utilisateurs
users = [
    {"username": "admin", "password": "Password123", "email": "admin@example.com", "age": 30},
    {"username": "user1", "password": "Password123", "email": "user1@example.com", "age": 25},
    {"username": "user2", "password": "Password123", "email": "user2@example.com", "age": 28},
    {"username": "user3", "password": "Password123", "email": "user3@example.com", "age": 22},
    {"username": "user4", "password": "Password123", "email": "user4@example.com", "age": 35},
]

# Supprimer les utilisateurs existants avec les mêmes noms d'utilisateur
for user_data in users:
    User.objects.filter(username=user_data["username"]).delete()
    print(f"Suppression de l'utilisateur existant {user_data['username']} (si existant)")

# Créer les nouveaux utilisateurs
created_users = []
for user_data in users:
    username = user_data["username"]
    password = user_data["password"]
    email = user_data["email"]
    age = user_data["age"]
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        age=age,
        can_be_contacted=True,
        can_data_be_shared=True
    )
    
    if username == "admin":
        user.is_staff = True
        user.is_superuser = True
        user.save()
    
    created_users.append(user)
    print(f"Utilisateur {username} créé avec succès")

# Créer un projet de démonstration
admin_user = User.objects.get(username="admin")
project = Project.objects.create(
    title="Projet de démonstration",
    description="Un projet créé pour tester l'API SoftDesk",
    type="BACKEND",
    author=admin_user
)

# Ajouter admin comme contributeur (auteur)
Contributor.objects.create(
    user=admin_user,
    project=project,
    role="AUTHOR"
)

# Ajouter user1 comme contributeur
user1 = User.objects.get(username="user1")
Contributor.objects.create(
    user=user1,
    project=project,
    role="CONTRIBUTOR"
)

# Créer une issue
issue = Issue.objects.create(
    title="Issue de démonstration",
    description="Une issue créée pour tester l'API",
    project=project,
    author=admin_user,
    assignee=user1,
    priority="MEDIUM",
    tag="BUG",
    status="TODO"
)

# Créer un commentaire
Comment.objects.create(
    description="Voici un commentaire de test sur cette issue.",
    author=admin_user,
    issue=issue
)

print("Création des données de démonstration terminée!")
