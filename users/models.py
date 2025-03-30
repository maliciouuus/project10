"""Modèles pour la gestion des utilisateurs.

Ce module définit le modèle d'utilisateur personnalisé qui étend le modèle
AbstractUser de Django avec des champs supplémentaires pour la conformité RGPD.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle d'utilisateur personnalisé.

    Étend le modèle AbstractUser de Django avec des champs supplémentaires
    pour respecter les exigences du RGPD et suivre les bonnes pratiques de
    gestion des données utilisateurs.

    Attributes:
        age: Âge de l'utilisateur (requis pour la vérification RGPD)
        can_be_contacted: Consentement pour être contacté
        can_data_be_shared: Consentement pour le partage des données
        created_time: Date et heure de création du compte
    """

    age = models.IntegerField(null=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Représentation textuelle de l'utilisateur.

        Returns:
            Nom d'utilisateur formaté
        """
        return f"{self.username}"
