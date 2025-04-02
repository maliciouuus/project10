"""Sérialiseurs pour l'application de projets.

Ce module contient tous les sérialiseurs pour l'application projects:
- ProjectListSerializer: Informations de base sur les projets pour les vues
  de liste
- ProjectDetailSerializer: Informations détaillées sur les projets avec
  données associées
- ContributorSerializer: Informations sur les contributeurs du projet
- IssueListSerializer: Informations de base sur les problèmes pour les vues
  de liste
- IssueDetailSerializer: Informations détaillées sur les problèmes avec
  commentaires
- CommentSerializer: Informations sur les commentaires
"""

from rest_framework import serializers
import django.contrib.auth

from users.serializers import UserSerializer
from .models import Project, Contributor, Issue, Comment


class ProjectListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la vue de liste des projets.

    Fournit des informations de base sur les projets adaptées aux affichages
    de liste.

    Attributes:
        id: Identifiant du projet
        title: Nom du projet
        description: Description du projet
        type: Type de projet
        author: Créateur du projet
        created_time: Horodatage de création du projet
    """

    class Meta:
        """Options Meta pour ProjectListSerializer."""

        model = Project
        fields = (
            "id",
            "title",
            "description",
            "type",
            "author",
            "created_time",
        )
        read_only_fields = ("author", "created_time")


class ProjectDetailSerializer(ProjectListSerializer):
    """Sérialiseur pour la vue détaillée des projets.

    Étend ProjectListSerializer avec des données associées supplémentaires,
    notamment les contributeurs et le nombre de problèmes.

    Attributs supplémentaires:
        contributors: Liste des contributeurs du projet
        issues_count: Nombre de problèmes dans le projet
    """

    author = UserSerializer(read_only=True)
    contributors = serializers.SerializerMethodField()
    issues_count = serializers.SerializerMethodField()

    class Meta(ProjectListSerializer.Meta):
        """Options Meta pour ProjectDetailSerializer."""

        fields = ProjectListSerializer.Meta.fields + (
            "contributors",
            "issues_count",
        )

    def get_contributors(self, obj):
        """Obtient tous les contributeurs d'un projet.

        Args:
            obj: Instance du projet

        Returns:
            Liste des données sérialisées des contributeurs
        """
        contributors = obj.contributors.all()
        return ContributorSerializer(contributors, many=True).data

    def get_issues_count(self, obj):
        """Obtient le nombre de problèmes d'un projet.

        Args:
            obj: Instance du projet

        Returns:
            Nombre entier de problèmes du projet
        """
        return obj.issues.count()


class ContributorSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les contributeurs de projets.

    Gère les informations des contributeurs, y compris leur rôle dans le
    projet.

    Attributes:
        id: Identifiant du contributeur
        user: Informations sur l'utilisateur
        project: Projet associé
        role: Rôle de l'utilisateur dans le projet
        created_time: Moment où l'utilisateur a été ajouté au projet
    """

    user = UserSerializer(read_only=True)

    class Meta:
        """Options Meta pour ContributorSerializer."""

        model = Contributor
        fields = ("id", "user", "project", "role", "created_time")
        read_only_fields = ("created_time",)


class ContributorCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création de contributeurs.

    Version simplifiée du ContributorSerializer où les champs project et user
    sont gérés dans le perform_create du ViewSet. Ce sérialiseur ne s'attend
    à recevoir que l'ID de l'utilisateur à ajouter comme contributeur.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=django.contrib.auth.get_user_model().objects.all()
    )

    class Meta:
        """Options Meta pour ContributorCreateSerializer."""

        model = Contributor
        fields = ("user", "project", "role")
        read_only_fields = ("project", "role")


class IssueListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la vue de liste des problèmes.

    Fournit des informations de base sur les problèmes adaptées aux affichages
    de liste.

    Attributes:
        id: Identifiant du problème
        title: Titre du problème
        description: Description du problème
        project: Projet associé
        author: Créateur du problème
        assignee: Utilisateur assigné au problème
        priority: Niveau de priorité du problème
        tag: Type de problème
        status: Statut actuel
        created_time: Horodatage de création
    """

    class Meta:
        """Options Meta pour IssueListSerializer."""

        model = Issue
        fields = (
            "id",
            "title",
            "description",
            "project",
            "author",
            "assignee",
            "priority",
            "tag",
            "status",
            "created_time",
        )
        read_only_fields = ("author", "created_time", "project")


class IssueDetailSerializer(IssueListSerializer):
    """Sérialiseur pour la vue détaillée des problèmes.

    Étend IssueListSerializer avec des données associées supplémentaires,
    notamment les commentaires.

    Attributs supplémentaires:
        comments: Liste des commentaires sur le problème
    """

    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta(IssueListSerializer.Meta):
        """Options Meta pour IssueDetailSerializer."""

        fields = IssueListSerializer.Meta.fields + ("comments",)

    def get_comments(self, obj):
        """Obtient tous les commentaires d'un problème.

        Args:
            obj: Instance du problème

        Returns:
            Liste des données sérialisées des commentaires
        """
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les commentaires sur les problèmes.

    Gère les informations des commentaires, y compris l'auteur et le problème
    associé.

    Attributes:
        id: Identifiant du commentaire
        description: Contenu du commentaire
        author: Créateur du commentaire
        issue: Problème associé
        uuid: Identifiant unique
        created_time: Horodatage de création
    """

    author = UserSerializer(read_only=True)

    class Meta:
        """Options Meta pour CommentSerializer."""

        model = Comment
        fields = (
            "id",
            "description",
            "author",
            "issue",
            "uuid",
            "created_time",
        )
        read_only_fields = ("author", "uuid", "created_time", "issue")
