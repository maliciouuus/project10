#!/usr/bin/env python3
"""Formulaires pour l'interface SoftDesk API."""

from cli.utils.ui_components import (
    show_header,
    show_error,
    show_info,
    show_warning,
    input_text,
    input_boolean,
    pause,
    show_json,
    create_table,
    display_table,
    text_input_form,
    option_form,
)


def login_form():
    """Formulaire de connexion.

    Returns:
        tuple: (username, password)
    """
    show_header("CONNEXION", subtitle="Authentification")

    username = input_text("Nom d'utilisateur")
    password = input_text("Mot de passe", password=True)

    return username, password


def register_form():
    """Formulaire d'inscription.

    Returns:
        dict: Données utilisateur
    """
    show_header("CRÉATION DE COMPTE", subtitle="Inscription")

    # Champs obligatoires
    fields = [
        ("Nom d'utilisateur", False, True),
        ("Email", False, True),
        ("Mot de passe", True, True),
        ("Confirmez le mot de passe", True, True),
    ]

    form_data = text_input_form(fields)

    # Vérification des mots de passe
    if form_data["mot_de_passe"] != form_data["confirmez_le_mot_de_passe"]:
        show_error("Les mots de passe ne correspondent pas")
        pause()
        return None

    # Âge
    try:
        age = int(input_text("Âge"))
    except ValueError:
        show_error("L'âge doit être un nombre")
        pause()
        return None

    # Champs facultatifs
    first_name = input_text("Prénom (facultatif)")
    last_name = input_text("Nom (facultatif)")

    # Consentement RGPD
    can_be_contacted = input_boolean("Acceptez-vous d'être contacté?")
    can_data_be_shared = input_boolean(
        "Acceptez-vous que vos données soient partagées?"
    )

    # Création de l'utilisateur
    user_data = {
        "username": form_data["nom_d'utilisateur"],
        "email": form_data["email"],
        "password": form_data["mot_de_passe"],
        "password2": form_data["confirmez_le_mot_de_passe"],
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "can_be_contacted": can_be_contacted,
        "can_data_be_shared": can_data_be_shared,
    }

    return user_data


def token_info_display(access_token, refresh_token, token_data):
    """Affiche les informations sur les tokens.

    Args:
        access_token: Le token d'accès
        refresh_token: Le token de rafraîchissement
        token_data: Les données décodées du token
    """
    show_header("INFORMATIONS DES TOKENS", subtitle="Sécurité")

    # Afficher access token
    if access_token:
        token = access_token
        show_info("\nAccess Token: {}...{}".format(token[:20], token[-20:]))

    # Afficher refresh token
    if refresh_token:
        token = refresh_token
        show_info("Refresh Token: {}...{}".format(token[:20], token[-20:]))

    # Informations détaillées
    if token_data and "decoded" in token_data:
        show_info("\nContenu décodé:")
        show_json(token_data["decoded"])

        if "exp_time" in token_data and token_data["exp_time"]:
            show_info("\nExpiration:")
            show_info(f"  Date: {token_data['exp_time']}")

            if (
                "time_left" in token_data
                and token_data["time_left"]
                and token_data["time_left"].total_seconds() > 0
            ):
                seconds = int(token_data["time_left"].total_seconds())
                minutes = int(seconds / 60)
                show_info(
                    f"  Temps restant: {seconds} secondes ({minutes} minutes)"
                )
            else:
                show_error("  Token expiré!")

    pause()


def create_project_form():
    """Formulaire de création de projet.

    Returns:
        dict: Données du projet
    """
    show_header("CRÉATION DE PROJET", subtitle="Projet")

    # Informations de base
    title = input_text("Titre du projet")
    description = input_text("Description")

    # Type de projet
    project_types = {
        "BACKEND": "Backend",
        "FRONTEND": "Frontend",
        "IOS": "iOS",
        "ANDROID": "Android",
    }

    project_type = option_form("Type de projet", project_types)

    # Création du projet
    project_data = {
        "title": title,
        "description": description,
        "type": project_type,
    }

    return project_data


def display_projects(projects_data):
    """Affiche la liste des projets.

    Args:
        projects_data: Données des projets

    Returns:
        str: ID du projet sélectionné ou None
    """
    show_header("LISTE DES PROJETS", subtitle="Projets")

    if projects_data.get("count", 0) == 0:
        show_warning("Vous n'avez aucun projet")
    else:
        projects = projects_data.get("results", [])

        # Création du tableau
        table = create_table(["ID", "Titre", "Type", "Date"])

        for project in projects:
            project_id = str(project.get("id", ""))
            title = project.get("title", "")
            project_type = project.get("type", "")
            created = project.get("created_time", "").split("T")[0]

            table.add_row(project_id, title, project_type, created)

        display_table(table)

        # Sélection d'un projet
        select = input_text(
            "\nSélectionner un projet (ID) ou appuyez sur Entrée pour revenir"
        )

        if select:
            try:
                project_id = int(select)
                show_info(f"Projet {project_id} sélectionné")
                return project_id
            except ValueError:
                show_error("ID invalide")

    pause()
    return None


def display_issues(issues_data, project_id):
    """Affiche la liste des issues d'un projet.

    Args:
        issues_data: Données des issues (peut être paginé)
        project_id: ID du projet

    Returns:
        int: ID de l'issue sélectionnée ou None
    """
    show_header(f"ISSUES DU PROJET {project_id}", subtitle="Issues")

    # Vérifier si nous avons des données
    if not issues_data:
        show_warning("Aucune issue trouvée")
        pause()
        return None

    # Déterminer si les données sont paginées
    if isinstance(issues_data, dict) and "results" in issues_data:
        issues = issues_data.get("results", [])
    elif isinstance(issues_data, list):
        issues = issues_data
    else:
        show_error(f"Format de données inattendu: {type(issues_data)}")
        pause()
        return None

    if not issues:
        show_warning("Aucune issue trouvée")
        pause()
        return None
    else:
        # Création du tableau
        table = create_table(["ID", "Titre", "Priorité", "Statut", "Type"])

        for issue in issues:
            issue_id = str(issue.get("id", ""))
            title = issue.get("title", "")
            priority = issue.get("priority", "")
            status = issue.get("status", "")
            tag = issue.get("tag", "")

            table.add_row(issue_id, title, priority, status, tag)

        display_table(table)

        # Sélection d'une issue
        select = input_text(
            "\nSélectionner une issue (ID) ou appuyez sur Entrée pour revenir"
        )

        if select:
            try:
                issue_id = int(select)
                show_info(f"Issue {issue_id} sélectionnée")
                return issue_id
            except ValueError:
                show_error("ID invalide")

    pause()
    return None


def create_issue_form(project_id, user_id):
    """Formulaire de création d'issue.

    Args:
        project_id: ID du projet
        user_id: ID de l'utilisateur

    Returns:
        dict: Données de l'issue
    """
    if not project_id:
        show_error("Aucun projet sélectionné")
        pause()
        return None

    show_header(
        f"CRÉATION D'ISSUE POUR LE PROJET {project_id}", subtitle="Issues"
    )

    # Informations de base
    title = input_text("Titre de l'issue")
    description = input_text("Description")

    # Priorité
    priorities = {"LOW": "Basse", "MEDIUM": "Moyenne", "HIGH": "Haute"}
    priority = option_form("Priorité", priorities)

    # Type d'issue
    tags = {"BUG": "Bug", "FEATURE": "Fonctionnalité", "TASK": "Tâche"}
    tag = option_form("Type d'issue", tags)

    # Assignation
    assignee_id = input_text(
        "ID de l'utilisateur assigné (vide pour vous-même)"
    )
    if not assignee_id:
        assignee_id = user_id

    # Création de l'issue
    issue_data = {
        "title": title,
        "description": description,
        "priority": priority,
        "tag": tag,
        "assignee": int(assignee_id),
    }

    return issue_data


def display_comments(comments_data, issue_id):
    """Affiche les commentaires d'une issue.

    Args:
        comments_data: Données des commentaires (peut être paginé)
        issue_id: ID de l'issue

    Returns:
        None
    """
    show_header(
        f"COMMENTAIRES DE L'ISSUE {issue_id}", subtitle="Communication"
    )

    # Vérifier si nous avons des données
    if not comments_data:
        show_warning("Aucun commentaire trouvé")
        pause()
        return

    # Déterminer si les données sont paginées
    if isinstance(comments_data, dict) and "results" in comments_data:
        comments = comments_data.get("results", [])
    elif isinstance(comments_data, list):
        comments = comments_data
    else:
        show_error(f"Format de données inattendu: {type(comments_data)}")
        pause()
        return

    if not comments:
        show_warning("Aucun commentaire trouvé")
    else:
        # Création du tableau
        table = create_table(["ID", "Auteur", "Description", "Date", "UUID"])

        for comment in comments:
            comment_id = str(comment.get("id", ""))
            author = (
                comment.get("author", {}).get("username", "")
                if comment.get("author")
                else ""
            )
            description = comment.get("description", "")
            # Tronquer la description si elle est trop longue
            if len(description) > 50:
                description = description[:47] + "..."
            created = (
                comment.get("created_time", "").split("T")[0]
                if comment.get("created_time")
                else ""
            )
            uuid = comment.get("uuid", "")

            table.add_row(comment_id, author, description, created, uuid)

        display_table(table)

    pause()


def create_comment_form(issue_id):
    """Formulaire de création de commentaire.

    Args:
        issue_id: ID de l'issue

    Returns:
        dict: Données du commentaire ou None si annulé
    """
    show_header(
        f"NOUVEAU COMMENTAIRE SUR L'ISSUE {issue_id}",
        subtitle="Communication",
    )

    # Description du commentaire
    description = input_text("Votre commentaire")

    if not description:
        show_error("Le commentaire ne peut pas être vide")
        pause()
        return None

    return {"description": description}


def display_contributors(contributors_data, project_id):
    """Affiche la liste des contributeurs d'un projet.

    Args:
        contributors_data: Données des contributeurs (peut être paginé)
        project_id: ID du projet

    Returns:
        None
    """
    show_header(
        f"CONTRIBUTEURS DU PROJET {project_id}", subtitle="Collaborateurs"
    )

    # Vérifier si nous avons des données
    if not contributors_data:
        show_warning("Aucun contributeur trouvé")
        pause()
        return

    # Déterminer si les données sont paginées
    if isinstance(contributors_data, dict) and "results" in contributors_data:
        contributors = contributors_data.get("results", [])
    elif isinstance(contributors_data, list):
        contributors = contributors_data
    else:
        show_error(f"Format de données inattendu: {type(contributors_data)}")
        pause()
        return

    if not contributors:
        show_warning("Aucun contributeur trouvé")
    else:
        # Création du tableau
        table = create_table(["ID", "Utilisateur", "Rôle", "Date d'ajout"])

        for contributor in contributors:
            contributor_id = str(contributor.get("id", ""))
            user = contributor.get("user", {})
            username = user.get("username", "") if user else ""
            role = contributor.get("role", "")
            created = (
                contributor.get("created_time", "").split("T")[0]
                if contributor.get("created_time")
                else ""
            )

            table.add_row(contributor_id, username, role, created)

        display_table(table)

    pause()


def add_contributor_form(project_id):
    """Formulaire d'ajout d'un contributeur.

    Args:
        project_id: ID du projet

    Returns:
        int: ID de l'utilisateur à ajouter comme contributeur
    """
    show_header(
        f"AJOUT DE CONTRIBUTEUR AU PROJET {project_id}",
        subtitle="Collaborateurs",
    )

    user_id = input_text("ID de l'utilisateur à ajouter")

    try:
        return int(user_id)
    except ValueError:
        show_error("L'ID doit être un nombre")
        pause()
        return None
