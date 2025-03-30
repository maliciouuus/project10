"""
Configuration des URLs pour le projet softdesk.

La liste `urlpatterns` achemine les URLs vers les vues. Pour plus d'informations,
voir: https://docs.djangoproject.com/en/5.0/topics/http/urls/
Exemples:
Vues fonctionnelles
    1. Ajouter un import:  from my_app import views
    2. Ajouter à urlpatterns:  path('', views.home, name='home')
Vues basées sur des classes
    1. Ajouter un import:  from other_app.views import Home
    2. Ajouter à urlpatterns:  path('', Home.as_view(), name='home')
Inclure un autre URLconf
    1. Importer la fonction include: from django.urls import include, path
    2. Ajouter à urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Configuration de la documentation de l'API avec Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="SoftDesk API",
        default_version="v1",
        description="API de gestion de projets et de suivi des problèmes",
        terms_of_service="https://www.softdesk.com/terms/",
        contact=openapi.Contact(email="contact@softdesk.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Interface d'administration
    path("admin/", admin.site.urls),
    # URLs d'authentification JWT
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    # URLs de l'API
    path("api/", include("projects.urls")),  # Routes de gestion de projets
    path(
        "api/auth/", include("users.urls")
    ),  # Routes d'authentification et utilisateurs
    # Documentation API
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
