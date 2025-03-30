"""Sérialiseurs pour la gestion des utilisateurs."""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription des utilisateurs.

    Gère la validation des données lors de l'inscription, notamment:
    - Unicité de l'email
    - Complexité du mot de passe
    - Confirmation du mot de passe
    - Vérification de l'âge (minimum 15 ans pour RGPD)
    - Recueil des consentements RGPD
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)
    age = serializers.IntegerField(required=True)
    can_be_contacted = serializers.BooleanField(required=True)
    can_data_be_shared = serializers.BooleanField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        """Classe Meta pour RegisterSerializer définissant le modèle et les champs."""

        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def validate(self, attrs):
        """Valide la correspondance des mots de passe et l'exigence d'âge minimum.

        Args:
            attrs: Données soumises pour validation

        Returns:
            Données validées

        Raises:
            ValidationError: Si les mots de passe ne correspondent pas ou si
                l'utilisateur a moins de 15 ans
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        if attrs["age"] < 15:
            raise serializers.ValidationError(
                {"age": "L'utilisateur doit avoir au moins 15 ans."}
            )
        return attrs

    def create(self, validated_data):
        """Crée et retourne un nouvel utilisateur.

        Args:
            validated_data: Données validées pour la création de l'utilisateur

        Returns:
            Instance du nouvel utilisateur créé
        """
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
            password=password,
            **validated_data,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle utilisateur.

    Utilisé pour la visualisation et la mise à jour des données utilisateur
    après l'inscription initiale.
    """

    class Meta:
        """Classe Meta pour UserSerializer définissant les champs exposés."""

        model = User
        fields = (
            "id",
            "username",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        )
        read_only_fields = ("created_time",)
