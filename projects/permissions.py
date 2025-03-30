"""Permissions pour l'application de gestion de projets.

Ce module définit les classes de permission personnalisées qui déterminent
quels utilisateurs peuvent accéder aux différentes ressources du projet.
"""

from rest_framework import permissions


class IsProjectContributor(permissions.BasePermission):
    """Permission permettant uniquement aux contributeurs d'un projet d'y accéder.

    Cette permission vérifie si l'utilisateur faisant la demande est un contributeur
    du projet concerné, quel que soit le type d'objet évalué (projet, problème
    ou commentaire).
    """

    def has_object_permission(self, request, view, obj):
        """Vérifie si l'utilisateur est contributeur du projet.

        Cette méthode détermine d'abord le projet associé à l'objet évalué,
        puis vérifie si l'utilisateur fait partie des contributeurs de ce projet.

        Args:
            request: La requête HTTP
            view: La vue appelée
            obj: L'objet pour lequel l'autorisation est vérifiée

        Returns:
            Boolean: True si l'utilisateur est un contributeur, False sinon
        """
        if hasattr(obj, "contributors"):
            # L'objet est un projet
            project = obj
        elif hasattr(obj, "project"):
            # L'objet est lié directement à un projet (ex: issue)
            project = obj.project
        else:
            # L'objet est lié indirectement à un projet (ex: commentaire)
            project = obj.issue.project
        return request.user in [
            contributor.user for contributor in project.contributors.all()
        ]


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission permettant uniquement aux auteurs d'un objet de le modifier.

    Cette permission autorise la lecture pour tous les utilisateurs,
    mais limite les opérations d'écriture (modification, suppression)
    uniquement à l'auteur de l'objet.
    """

    def has_object_permission(self, request, view, obj):
        """Vérifie si l'utilisateur est l'auteur de l'objet.

        Args:
            request: La requête HTTP
            view: La vue appelée
            obj: L'objet pour lequel l'autorisation est vérifiée

        Returns:
            Boolean: True si la méthode est sécurisée (GET, HEAD, OPTIONS)
                    ou si l'utilisateur est l'auteur de l'objet
        """
        if request.method in permissions.SAFE_METHODS:
            # Autoriser les méthodes de lecture pour tous
            return True
        # Vérifier que l'utilisateur est bien l'auteur pour les modifications
        return obj.author == request.user
