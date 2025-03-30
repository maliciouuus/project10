"""Vues pour la gestion des utilisateurs."""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs.

    Cette vue permet la création d'un nouveau compte utilisateur.
    Aucune authentification n'est requise pour accéder à cette vue.
    """

    authentication_classes = []  # Pas d'authentification pour l'inscription
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """Crée un nouvel utilisateur.

        Gère la validation des données, la création de l'utilisateur et
        la génération d'une réponse appropriée.

        Args:
            request: Requête HTTP contenant les données d'inscription

        Returns:
            Réponse HTTP avec les données utilisateur ou les erreurs
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.save()
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "Utilisateur créé avec succès",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour les détails, la mise à jour et la suppression d'un utilisateur.

    Cette vue permet à un utilisateur authentifié de consulter, modifier
    ou supprimer son propre compte. L'authentification JWT est requise.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """Récupère l'utilisateur actuel.

        Returns:
            L'instance de l'utilisateur connecté
        """
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        """Supprime l'utilisateur actuel.

        Vérifie que l'utilisateur tente bien de supprimer son propre compte,
        ce qui est une mesure de sécurité supplémentaire.

        Args:
            request: Requête HTTP

        Returns:
            Réponse HTTP avec le statut approprié
        """
        user = self.get_object()
        if user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
