"""Configuration des URLs pour l'application utilisateurs."""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import RegisterView, UserDetailView

urlpatterns = [
    # Authentification
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Gestion des utilisateurs
    path("signup/", RegisterView.as_view(), name="signup"),
    path("account/", UserDetailView.as_view(), name="account"),
]
