from rest_framework import permissions


class AllowAnyForRegisterAndToken(permissions.BasePermission):
    def has_permission(self, request, view):
        # Liste des chemins qui doivent être publics
        public_paths = ["signup", "token", "token/refresh"]

        # Vérifier si le chemin de la requête contient l'un des chemins publics
        return any(path in request.path for path in public_paths)
