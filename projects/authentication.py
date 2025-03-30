"""Module d'authentification personnalisé pour l'API.

Ce module définit une classe d'authentification JWT personnalisée pour
sécuriser les endpoints de l'API et fournir une gestion d'erreurs claire.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CustomJWTAuthentication(JWTAuthentication):
    """Authentification JWT personnalisée avec validation et gestion d'erreurs.

    Cette classe étend l'authentification JWT standard pour fournir une validation
    plus stricte des tokens et des messages d'erreur plus explicites.
    Elle garantit que chaque requête comporte un token JWT valide avec le
    format approprié.
    """

    def authenticate(self, request):
        """Authentifie une requête en validant son token JWT.

        Cette méthode extrait le token JWT de l'en-tête Authorization,
        vérifie son format, valide sa signature et son expiration,
        puis retourne l'utilisateur associé.

        Args:
            request: La requête HTTP à authentifier

        Returns:
            Tuple (user, token): L'utilisateur authentifié et le token validé

        Raises:
            AuthenticationFailed: Si le token est absent, invalide ou expiré
        """
        header = get_authorization_header(request)
        if not header:
            raise AuthenticationFailed(_("No authentication token provided"))

        try:
            header_decoded = header.decode("utf-8")
            if not header_decoded.startswith("Bearer "):
                raise AuthenticationFailed(
                    _("Invalid authentication token format")
                )

            raw_token = header_decoded.split(" ")[1]
            if not raw_token:
                raise AuthenticationFailed(_("Empty token"))

            # Validation explicite du token
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except UnicodeError:
            raise AuthenticationFailed(_("Invalid token header"))
        except InvalidToken:
            raise AuthenticationFailed(_("Token is invalid or expired"))
        except TokenError:
            raise AuthenticationFailed(_("Invalid token"))
        except Exception:
            raise AuthenticationFailed(_("Authentication failed"))
