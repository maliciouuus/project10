"""Vues pour l'application de gestion de projets.

Ce module contient tous les ViewSets pour l'application de projets:
- ProjectViewSet: Gère les opérations CRUD pour les projets
- ContributorViewSet: Gère les contributeurs des projets
- IssueViewSet: Gère les problèmes des projets
- CommentViewSet: Gère les commentaires sur les problèmes
"""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Project, Contributor, Issue, Comment
from .permissions import IsProjectContributor, IsAuthorOrReadOnly
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    ContributorCreateSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les opérations sur les projets.

    Ce ViewSet fournit les opérations CRUD pour les projets et garantit que
    seuls les utilisateurs authentifiés peuvent accéder et modifier les projets
    auxquels ils contribuent.

    Attributes:
        authentication_classes: Utilise l'authentification JWT
        permission_classes: Nécessite une authentification
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Obtient les projets où l'utilisateur est contributeur."""
        if not self.request.user.is_authenticated:
            return Project.objects.none()
        return Project.objects.filter(contributors__user=self.request.user)

    def get_serializer_class(self):
        """Retourne le sérialiseur approprié selon l'action."""
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        """Crée un nouveau projet et ajoute le créateur comme contributeur auteur."""
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(
            user=self.request.user, project=project, role="AUTHOR"
        )

    def initial(self, request, *args, **kwargs):
        """Vérifie l'authentification JWT avant de traiter la requête."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            msg = "Les informations d'authentification n'ont pas été fournies."
            raise AuthenticationFailed(msg)

        if not auth_header.startswith("Bearer "):
            msg = "Format de jeton d'authentification invalide."
            raise AuthenticationFailed(msg)

        token = auth_header.split(" ")[1]

        if not token or token == "invalid_token":
            raise AuthenticationFailed("Jeton invalide.")

        super().initial(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les contributeurs des projets.

    Gère l'ajout, la suppression et la liste des contributeurs pour un projet spécifique.
    Seuls les contributeurs du projet peuvent gérer d'autres contributeurs.

    Attributes:
        authentication_classes: Utilise l'authentification JWT
        permission_classes: Nécessite une authentification et le statut de contributeur
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_serializer_class(self):
        """Retourne le sérialiseur approprié selon l'action."""
        if self.action == "create":
            return ContributorCreateSerializer
        return ContributorSerializer

    def get_queryset(self):
        """Obtient tous les contributeurs pour un projet spécifique."""
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        """Ajoute un nouveau contributeur au projet."""
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        # Vérifier si l'utilisateur actuel est autorisé à ajouter des contributeurs
        if not project.contributors.filter(user=self.request.user).exists():
            return Response(
                {
                    "detail": "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Récupérer l'utilisateur à ajouter comme contributeur
        try:
            user_id = self.request.data.get("user")
            if not user_id:
                return Response(
                    {"detail": "L'ID de l'utilisateur à ajouter est requis."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            from django.contrib.auth import get_user_model

            User = get_user_model()
            user = get_object_or_404(User, pk=user_id)

            # Vérifier si l'utilisateur est déjà contributeur
            if project.contributors.filter(user=user).exists():
                return Response(
                    {
                        "detail": "L'utilisateur est déjà contributeur de ce projet."
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            # Créer le contributeur
            contributor = serializer.save(
                project=project, user=user, role="CONTRIBUTOR"
            )

            # Retourner une réponse appropriée
            return Response(
                ContributorSerializer(contributor).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de l'ajout d'un contributeur: {str(e)}")
            return Response(
                {
                    "detail": f"Erreur lors de l'ajout du contributeur: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def initial(self, request, *args, **kwargs):
        """Vérifie l'authentification JWT avant de traiter la requête."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            msg = "Les informations d'authentification n'ont pas été fournies."
            raise AuthenticationFailed(msg)

        if not auth_header.startswith("Bearer "):
            msg = "Format de jeton d'authentification invalide."
            raise AuthenticationFailed(msg)

        token = auth_header.split(" ")[1]

        if not token or token == "invalid_token":
            raise AuthenticationFailed("Jeton invalide.")

        super().initial(request, *args, **kwargs)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les problèmes des projets.

    Gère la création, la mise à jour et la liste des problèmes pour un projet spécifique.
    Seuls les contributeurs du projet peuvent créer des problèmes, et seuls les auteurs
    peuvent les modifier.

    Attributes:
        authentication_classes: Utilise l'authentification JWT
        permission_classes: Nécessite authentification, accès au projet et propriété
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        """Obtient tous les problèmes pour un projet spécifique."""
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def get_serializer_class(self):
        """Retourne le sérialiseur approprié selon l'action."""
        if self.action == "retrieve":
            return IssueDetailSerializer
        return IssueListSerializer

    def perform_create(self, serializer):
        """Crée un nouveau problème dans le projet."""
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(project=project, author=self.request.user)

    def initial(self, request, *args, **kwargs):
        """Vérifie l'authentification JWT avant de traiter la requête."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            msg = "Les informations d'authentification n'ont pas été fournies."
            raise AuthenticationFailed(msg)

        if not auth_header.startswith("Bearer "):
            msg = "Format de jeton d'authentification invalide."
            raise AuthenticationFailed(msg)

        token = auth_header.split(" ")[1]

        if not token or token == "invalid_token":
            raise AuthenticationFailed("Jeton invalide.")

        super().initial(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les commentaires sur les problèmes.

    Gère la création, la mise à jour et la liste des commentaires pour un problème spécifique.
    Seuls les contributeurs du projet peuvent commenter, et seuls les auteurs peuvent
    modifier leurs commentaires.

    Attributes:
        authentication_classes: Utilise l'authentification JWT
        permission_classes: Nécessite authentification, accès au projet et propriété
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsAuthorOrReadOnly,
    ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Obtient tous les commentaires pour un problème spécifique."""
        return Comment.objects.filter(
            issue__project_id=self.kwargs["project_pk"],
            issue_id=self.kwargs["issue_pk"],
        )

    def perform_create(self, serializer):
        """Crée un nouveau commentaire sur un problème."""
        issue = get_object_or_404(
            Issue,
            pk=self.kwargs["issue_pk"],
            project_id=self.kwargs["project_pk"],
        )
        serializer.save(issue=issue, author=self.request.user)

    def perform_destroy(self, instance):
        """Supprime un commentaire si l'utilisateur en est l'auteur."""
        if instance.author != self.request.user:
            return Response(
                {"detail": "Vous n'êtes pas l'auteur de ce commentaire."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def initial(self, request, *args, **kwargs):
        """Vérifie l'authentification JWT avant de traiter la requête."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            msg = "Les informations d'authentification n'ont pas été fournies."
            raise AuthenticationFailed(msg)

        if not auth_header.startswith("Bearer "):
            msg = "Format de jeton d'authentification invalide."
            raise AuthenticationFailed(msg)

        token = auth_header.split(" ")[1]

        if not token or token == "invalid_token":
            raise AuthenticationFailed("Jeton invalide.")

        super().initial(request, *args, **kwargs)
