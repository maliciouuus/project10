"""Configuration des URLs pour l'application de projets.

Ce module définit le routage des URLs pour toutes les vues liées aux projets
en utilisant des routeurs imbriqués pour gérer la relation hiérarchique entre
projets, problèmes et commentaires.

La structure des URLs suit ce modèle:
- /projects/ - Liste et création de projets
- /projects/{id}/ - Détail, mise à jour, suppression d'un projet
- /projects/{id}/users/ - Contributeurs d'un projet
- /projects/{id}/issues/ - Problèmes d'un projet
- /projects/{id}/issues/{id}/comments/ - Commentaires sur un problème
"""

from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.permissions import IsAuthenticated

from .views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)
from .authentication import CustomJWTAuthentication

# Configuration par défaut pour tous les routeurs
router_config = {
    "DEFAULT_AUTHENTICATION_CLASSES": [CustomJWTAuthentication],
    "DEFAULT_PERMISSION_CLASSES": [IsAuthenticated],
}

# Router principal pour les projets
router = routers.SimpleRouter()
router.register(r"projects", ProjectViewSet, basename="project")

# Router pour les contributeurs et les issues (imbriqué dans les projets)
projects_router = routers.NestedSimpleRouter(
    router, r"projects", lookup="project"
)
projects_router.register(
    r"users", ContributorViewSet, basename="project-users"
)
projects_router.register(r"issues", IssueViewSet, basename="project-issues")

# Router pour les commentaires (imbriqué dans les issues)
issues_router = routers.NestedSimpleRouter(
    projects_router, r"issues", lookup="issue"
)
issues_router.register(r"comments", CommentViewSet, basename="issue-comments")

# Application des configurations aux routeurs
for router_instance in [router, projects_router, issues_router]:
    router_instance.authentication_classes = router_config[
        "DEFAULT_AUTHENTICATION_CLASSES"
    ]
    router_instance.permission_classes = router_config[
        "DEFAULT_PERMISSION_CLASSES"
    ]

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
