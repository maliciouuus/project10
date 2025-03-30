"""Modèles pour la gestion des projets.

Ce module contient tous les modèles pour l'application projects:
- Project: Modèle principal de projet
- Contributor: Relie les utilisateurs aux projets avec des rôles
- Issue: Suit les problèmes/tâches du projet
- Comment: Stocke les commentaires sur les problèmes
"""

from django.conf import settings
from django.db import models
import uuid


class Project(models.Model):
    """Modèle de projet pour la gestion des projets de développement logiciel.

    Un projet peut avoir plusieurs contributeurs et problèmes. Le créateur du
    projet est automatiquement défini comme son auteur et premier contributeur.

    Attributes:
        title: Nom du projet
        description: Description détaillée du projet
        type: Type de projet (Backend, Frontend, iOS, Android)
        author: Utilisateur qui a créé le projet
        created_time: Horodatage de la création du projet
    """

    TYPE_CHOICES = [
        ("BACKEND", "Back-end"),
        ("FRONTEND", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne la représentation textuelle du projet."""
        return f"{self.title}"


class Contributor(models.Model):
    """Modèle de contributeur reliant les utilisateurs aux projets.

    Suit le rôle de chaque utilisateur dans un projet. Un utilisateur peut être
    soit un auteur (créateur du projet), soit un contributeur.

    Attributes:
        user: L'utilisateur contributeur
        project: Le projet auquel l'utilisateur contribue
        role: Rôle de l'utilisateur dans le projet (Auteur/Contributeur)
        created_time: Moment où l'utilisateur a été ajouté au projet
    """

    ROLE_CHOICES = [
        ("AUTHOR", "Author"),
        ("CONTRIBUTOR", "Contributor"),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    role = models.CharField(
        max_length=11, choices=ROLE_CHOICES, default="CONTRIBUTOR"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Options Meta pour le modèle Contributor."""

        unique_together = ("user", "project")

    def __str__(self):
        """Retourne la représentation textuelle de la contribution."""
        return f"{self.user.username} - {self.project.title}"


class Issue(models.Model):
    """Modèle de problème pour suivre les tâches et problèmes du projet.

    Les problèmes peuvent être assignés aux contributeurs du projet et peuvent
    avoir plusieurs commentaires. Ils suivent la priorité, le type et le statut
    des tâches.

    Attributes:
        title: Titre du problème
        description: Description détaillée du problème
        project: Projet auquel appartient le problème
        author: Utilisateur qui a créé le problème
        assignee: Utilisateur assigné pour résoudre le problème
        priority: Priorité du problème (Basse/Moyenne/Haute)
        tag: Type de problème (Bug/Fonctionnalité/Tâche)
        status: Statut actuel (À faire/En cours/Terminé)
        created_time: Moment où le problème a été créé
    """

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]

    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
        null=True,
    )
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=7, choices=TAG_CHOICES)
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default="TODO"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne la représentation textuelle du problème."""
        return f"{self.title}"


class Comment(models.Model):
    """Modèle de commentaire pour les discussions sur les problèmes.

    Permet aux utilisateurs de discuter des problèmes en ajoutant des
    commentaires. Chaque commentaire possède un UUID unique pour une
    identification sécurisée.

    Attributes:
        description: Contenu du commentaire
        author: Utilisateur qui a écrit le commentaire
        issue: Problème sur lequel porte le commentaire
        uuid: Identifiant unique pour le commentaire
        created_time: Moment où le commentaire a été publié
    """

    description = models.TextField(max_length=2048)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_comments",
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne la représentation textuelle du commentaire."""
        return f"Commentaire de {self.author.username} sur {self.issue.title}"
