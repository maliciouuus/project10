#!/usr/bin/env python3
"""Interface ultra minimaliste pour l'API SoftDesk."""

from cli.api.softdesk_client import SoftDeskAPI
from cli.utils.ui_components import (
    show_header,
    show_categories,
    show_success,
    show_error,
    input_text,
    pause,
)
from cli.utils.forms import (
    login_form,
    register_form,
    token_info_display,
    create_project_form,
    display_projects,
    create_issue_form,
    display_contributors,
    add_contributor_form,
    display_issues,
    display_comments,
    create_comment_form,
)


class SoftDeskMini:
    """Application minimaliste pour SoftDesk API."""

    def __init__(self):
        """Initialise l'application."""
        self.api = SoftDeskAPI()
        self.running = True

    def get_header_info(self):
        """Récupère les informations à afficher dans l'en-tête."""
        info = {}

        if self.api.is_authenticated():
            info["Utilisateur"] = self.api.username
            if self.api.project_id:
                info["Projet"] = self.api.project_id
            if self.api.issue_id:
                info["Issue"] = self.api.issue_id

        return info

    def get_menu_categories(self):
        """Retourne les catégories du menu selon l'état de l'application."""
        categories = {}

        # Menu Authentification
        auth_options = {}
        if not self.api.is_authenticated():
            auth_options = {"1": "Se connecter", "2": "Créer un compte"}
        else:
            auth_options = {
                "3": "Se déconnecter",
                "4": "Informations sur les tokens",
            }

        categories["Authentification"] = auth_options

        # Menu Projets (seulement si authentifié)
        if self.api.is_authenticated():
            categories["Gestion des projets"] = {
                "5": "Créer un projet",
                "6": "Liste des projets",
            }

            # Menu Contributeurs (seulement si projet sélectionné)
            if self.api.project_id:
                categories["Gestion des contributeurs"] = {
                    "7": "Liste des contributeurs",
                    "8": "Ajouter un contributeur",
                }

        # Menu Issues (seulement si projet sélectionné)
        if self.api.is_authenticated() and self.api.project_id:
            categories["Gestion des issues"] = {
                "9": "Créer une issue",
                "10": "Liste des issues",
            }

        # Menu Commentaires (seulement si une issue est sélectionnée)
        if (
            self.api.is_authenticated()
            and self.api.project_id
            and self.api.issue_id
        ):
            categories["Gestion des commentaires"] = {
                "11": "Liste des commentaires",
                "12": "Ajouter un commentaire",
            }

        # Option de sortie
        categories["Général"] = {"0": "Quitter"}

        return categories

    def handle_login(self):
        """Gère la connexion de l'utilisateur."""
        username, password = login_form()
        success, message = self.api.login(username, password)

        if success:
            show_success(message)
        else:
            show_error(message)

        pause()

    def handle_register(self):
        """Gère l'inscription d'un nouvel utilisateur."""
        user_data = register_form()
        if not user_data:
            return

        success, message = self.api.register(user_data)

        if success:
            show_success(message)
        else:
            show_error(message)

        pause()

    def handle_logout(self):
        """Gère la déconnexion de l'utilisateur."""
        success, message = self.api.logout()

        if success:
            show_success(message)
        else:
            show_error(message)

        pause()

    def handle_token_info(self):
        """Affiche les informations sur les tokens."""
        success, data = self.api.token_info()
        token_info_display(
            self.api.access_token,
            self.api.refresh_token,
            data if success else None,
        )

    def handle_create_project(self):
        """Gère la création d'un projet."""
        project_data = create_project_form()
        success, data = self.api.create_project(project_data)

        if success:
            msg = (
                f"Projet '{project_data['title']}' "
                f"créé avec l'ID {data.get('id')}"
            )
            show_success(msg)
        else:
            show_error(data)

        pause()

    def handle_list_projects(self):
        """Affiche la liste des projets et permet d'en sélectionner un."""
        success, data = self.api.list_projects()

        if success:
            project_id = display_projects(data)
            if project_id:
                self.api.project_id = project_id
                # Réinitialiser l'issue sélectionnée si on change de projet
                self.api.issue_id = None
        else:
            show_error(data)
            pause()

    def handle_list_contributors(self):
        """Affiche la liste des contributeurs du projet courant."""
        if not self.api.project_id:
            show_error("Aucun projet sélectionné")
            pause()
            return

        success, data = self.api.list_contributors()

        if success:
            display_contributors(data, self.api.project_id)
        else:
            show_error(data)
            pause()

    def handle_add_contributor(self):
        """Ajoute un contributeur au projet courant."""
        if not self.api.project_id:
            show_error("Aucun projet sélectionné")
            pause()
            return

        user_id = add_contributor_form(self.api.project_id)
        if not user_id:
            return

        success, message = self.api.add_contributor(user_id)

        if success:
            show_success(message)
        else:
            show_error(message)

        pause()

    def handle_create_issue(self):
        """Gère la création d'une issue."""
        issue_data = create_issue_form(self.api.project_id, self.api.user_id)
        if not issue_data:
            return

        success, data = self.api.create_issue(issue_data)

        if success:
            msg = (
                f"Issue '{issue_data['title']}' "
                f"créée avec l'ID {data.get('id')}"
            )
            show_success(msg)
        else:
            show_error(data)

        pause()

    def handle_list_issues(self):
        """Affiche la liste des issues et permet d'en sélectionner une."""
        if not self.api.project_id:
            show_error("Aucun projet sélectionné")
            pause()
            return

        success, data = self.api.list_issues()

        if success:
            issue_id = display_issues(data, self.api.project_id)
            if issue_id:
                self.api.issue_id = issue_id
        else:
            show_error(data)
            pause()

    def handle_list_comments(self):
        """Affiche la liste des commentaires de l'issue courante."""
        if not self.api.project_id:
            show_error("Aucun projet sélectionné")
            pause()
            return

        if not self.api.issue_id:
            show_error("Aucune issue sélectionnée")
            pause()
            return

        success, data = self.api.list_comments()

        if success:
            display_comments(data, self.api.issue_id)
        else:
            show_error(data)
            pause()

    def handle_create_comment(self):
        """Gère la création d'un commentaire."""
        if not self.api.project_id:
            show_error("Aucun projet sélectionné")
            pause()
            return

        if not self.api.issue_id:
            show_error("Aucune issue sélectionnée")
            pause()
            return

        comment_data = create_comment_form(self.api.issue_id)
        if not comment_data:
            return

        success, data = self.api.create_comment(comment_data)

        if success:
            show_success("Commentaire ajouté avec succès")
        else:
            show_error(data)

        pause()

    def main_loop(self):
        """Boucle principale de l'application."""
        while self.running:
            # Afficher l'en-tête
            show_header(
                "SoftDesk API Mini",
                subtitle="v1.0",
                info=self.get_header_info(),
            )

            # Afficher les catégories du menu
            categories = self.get_menu_categories()
            show_categories(categories)

            # Demander le choix de l'utilisateur
            choice = input_text("\nVotre choix")

            # Traiter le choix
            if choice == "0":
                self.running = False
            elif choice == "1" and not self.api.is_authenticated():
                self.handle_login()
            elif choice == "2" and not self.api.is_authenticated():
                self.handle_register()
            elif choice == "3" and self.api.is_authenticated():
                self.handle_logout()
            elif choice == "4" and self.api.is_authenticated():
                self.handle_token_info()
            elif choice == "5" and self.api.is_authenticated():
                self.handle_create_project()
            elif choice == "6" and self.api.is_authenticated():
                self.handle_list_projects()
            elif (
                choice == "7"
                and self.api.is_authenticated()
                and self.api.project_id
            ):
                self.handle_list_contributors()
            elif (
                choice == "8"
                and self.api.is_authenticated()
                and self.api.project_id
            ):
                self.handle_add_contributor()
            elif (
                choice == "9"
                and self.api.is_authenticated()
                and self.api.project_id
            ):
                self.handle_create_issue()
            elif (
                choice == "10"
                and self.api.is_authenticated()
                and self.api.project_id
            ):
                self.handle_list_issues()
            elif (
                choice == "11"
                and self.api.is_authenticated()
                and self.api.project_id
                and self.api.issue_id
            ):
                self.handle_list_comments()
            elif (
                choice == "12"
                and self.api.is_authenticated()
                and self.api.project_id
                and self.api.issue_id
            ):
                self.handle_create_comment()

    def run(self):
        """Lance l'application."""
        try:
            self.main_loop()
        except KeyboardInterrupt:
            print("\nFermeture de l'application...")
        except Exception as e:
            show_error(f"Erreur inattendue: {str(e)}")
        finally:
            print("Au revoir!")


if __name__ == "__main__":
    app = SoftDeskMini()
    app.run()
