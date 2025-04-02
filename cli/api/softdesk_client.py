#!/usr/bin/env python3
"""Client API SoftDesk simplifié."""

import os
import json
import requests
import jwt
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
CONFIG_FILE = os.path.expanduser("~/.softdesk_config.json")


class SoftDeskAPI:
    """Client API SoftDesk simplifié."""

    def __init__(self):
        self.api_url = API_URL
        self.access_token = None
        self.refresh_token = None
        self.username = None
        self.user_id = None
        self.project_id = None
        self.issue_id = None
        self.load_config()

    def load_config(self):
        """Charge la configuration depuis le fichier."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    self.access_token = config.get("access_token")
                    self.refresh_token = config.get("refresh_token")
                    self.username = config.get("username")
                    self.user_id = config.get("user_id")
                return True, "Configuration chargée"
            return False, "Aucune configuration trouvée"
        except Exception as e:
            return False, f"Erreur de chargement de la config: {e}"

    def save_config(self):
        """Sauvegarde la configuration."""
        try:
            config = {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "username": self.username,
                "user_id": self.user_id,
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)
            return True, "Configuration sauvegardée"
        except Exception as e:
            return False, f"Erreur de sauvegarde de la config: {e}"

    def is_authenticated(self):
        """Vérifie si l'utilisateur est authentifié."""
        return bool(self.access_token)

    def get_headers(self):
        """Retourne les en-têtes HTTP avec le token d'authentification."""
        if self.access_token:
            return {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
        return {"Content-Type": "application/json"}

    def login(self, username, password):
        """Authentifie l'utilisateur et récupère les tokens."""
        try:
            # Afficher les données de connexion pour débogage
            print(f"Tentative de connexion à {self.api_url}/api/token/")
            print(f'Données: {{"username": "{username}", "password": "***"}}')

            response = requests.post(
                f"{self.api_url}/api/token/",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
            )

            # Afficher plus d'informations sur la réponse pour le débogage
            print(f"Status code: {response.status_code}")
            print(f"Réponse: {response.text}")

            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access")
                self.refresh_token = data.get("refresh")
                self.username = username

                # Récupérer l'ID utilisateur
                user_response = requests.get(
                    f"{self.api_url}/api/auth/account/",
                    headers=self.get_headers(),
                )

                if user_response.status_code == 200:
                    self.user_id = user_response.json().get("id")

                self.save_config()
                return True, "Connexion réussie"
            else:
                # Message d'erreur plus détaillé
                error_detail = ""
                try:
                    error_detail = response.json().get("detail", "")
                except json.JSONDecodeError:
                    error_detail = response.text

                error_msg = (
                    f"Échec de connexion: {response.status_code} - "
                    f"{error_detail}"
                )
                return False, error_msg
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def logout(self):
        """Déconnecte l'utilisateur."""
        if self.refresh_token:
            try:
                requests.post(
                    f"{self.api_url}/api/token/blacklist/",
                    json={"refresh": self.refresh_token},
                )
            except Exception:
                pass

        self.access_token = None
        self.refresh_token = None
        self.username = None
        self.user_id = None
        self.save_config()
        return True, "Déconnexion réussie"

    def register(self, user_data):
        """Enregistre un nouvel utilisateur."""
        try:
            response = requests.post(
                f"{self.api_url}/api/auth/signup/", json=user_data
            )

            if response.status_code == 201:
                data = response.json()
                self.user_id = data.get("user", {}).get("id")
                self.username = user_data.get("username")
                return True, "Compte créé avec succès"
            else:
                return False, f"Échec de création: {response.json()}"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def list_projects(self):
        """Liste tous les projets."""
        try:
            response = requests.get(
                f"{self.api_url}/api/projects/", headers=self.get_headers()
            )

            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Échec: {response.status_code}"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def create_project(self, project_data):
        """Crée un nouveau projet."""
        try:
            response = requests.post(
                f"{self.api_url}/api/projects/",
                headers=self.get_headers(),
                json=project_data,
            )

            if response.status_code == 201:
                data = response.json()
                self.project_id = data.get("id")
                return True, data
            else:
                return False, f"Échec: {response.json()}"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def create_issue(self, issue_data):
        """Crée une nouvelle issue."""
        if not self.project_id:
            return False, "Aucun projet sélectionné"

        try:
            url = f"{self.api_url}/api/projects/{self.project_id}/issues/"
            response = requests.post(
                url,
                headers=self.get_headers(),
                json=issue_data,
            )

            if response.status_code == 201:
                data = response.json()
                self.issue_id = data.get("id")
                return True, data
            else:
                return False, f"Échec: {response.json()}"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def list_issues(self, project_id=None):
        """Liste toutes les issues d'un projet.

        Args:
            project_id: ID du projet. Si non spécifié, utilise self.project_id

        Returns:
            (success, data): Tuple avec un booléen de succès et données/message
        """
        if not project_id and not self.project_id:
            return False, "Aucun projet sélectionné"

        project_id = project_id or self.project_id

        try:
            url = f"{self.api_url}/api/projects/{project_id}/issues/"
            response = requests.get(
                url,
                headers=self.get_headers(),
            )

            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = (
                    f"Échec de récupération des issues: {response.status_code}"
                )
                return False, error_msg
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def list_contributors(self, project_id=None):
        """Liste tous les contributeurs d'un projet.

        Args:
            project_id: ID du projet. Si non spécifié, utilise self.project_id

        Returns:
            (success, data): Tuple avec booléen de succès et données/message
        """
        if not project_id and not self.project_id:
            return False, "Aucun projet sélectionné"

        project_id = project_id or self.project_id

        try:
            print(
                f"Récupération des contributeurs pour le projet {project_id}"
            )
            url = f"{self.api_url}/api/projects/{project_id}/users/"
            response = requests.get(
                url,
                headers=self.get_headers(),
            )

            print(f"Status code: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Type de données reçu: {type(data)}")

                    # Vérifier le format des données
                    is_list = isinstance(data, list)
                    is_paginated = isinstance(data, dict) and "results" in data

                    if is_list or is_paginated:
                        return True, data
                    else:
                        print(f"Format de données inattendu: {data}")
                        return False, f"Format de données inattendu: {data}"
                except ValueError as e:
                    print(f"Erreur de décodage JSON: {str(e)}")
                    print(f"Contenu de la réponse: {response.text}")
                    return False, f"Erreur de décodage JSON: {str(e)}"
            else:
                print(f"Réponse: {response.text}")
                error_msg = (
                    f"Échec de récupération des contributeurs: "
                    f"{response.status_code}"
                )
                return False, error_msg
        except Exception as e:
            print(f"Exception: {str(e)}")
            return False, f"Erreur: {str(e)}"

    def add_contributor(self, user_id, project_id=None):
        """Ajoute un utilisateur comme contributeur à un projet.

        Args:
            user_id: ID de l'utilisateur à ajouter
            project_id: ID du projet. Si non spécifié, utilise self.project_id

        Returns:
            (success, data): Tuple avec booléen de succès et données/message
        """
        if not project_id and not self.project_id:
            return False, "Aucun projet sélectionné"

        project_id = project_id or self.project_id

        try:
            url = f"{self.api_url}/api/projects/{project_id}/users/"
            response = requests.post(
                url,
                headers=self.get_headers(),
                json={"user": user_id},
            )

            print(f"Status code: {response.status_code}")
            print(f"Réponse: {response.text}")

            if response.status_code in (201, 200):
                return True, "Contributeur ajouté avec succès"
            else:
                error_detail = ""
                try:
                    error_detail = response.json()
                except json.JSONDecodeError:
                    error_detail = response.text

                error_msg = f"Échec d'ajout du contributeur: {error_detail}"
                return False, error_msg
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def list_comments(self, issue_id=None):
        """Liste tous les commentaires d'une issue.

        Args:
            issue_id: ID de l'issue. Si non spécifié, utilise self.issue_id

        Returns:
            (success, data): Tuple avec booléen de succès et données/message
        """
        if not self.project_id:
            return False, "Aucun projet sélectionné"

        if not issue_id and not self.issue_id:
            return False, "Aucune issue sélectionnée"

        issue_id = issue_id or self.issue_id

        try:
            url = (
                f"{self.api_url}/api/projects/{self.project_id}/issues/"
                f"{issue_id}/comments/"
            )
            response = requests.get(
                url,
                headers=self.get_headers(),
            )

            print(f"Status code: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()

                    # Vérifier le format des données
                    is_list = isinstance(data, list)
                    is_paginated = isinstance(data, dict) and "results" in data

                    if is_list or is_paginated:
                        return True, data
                    else:
                        print(f"Format de données inattendu: {data}")
                        return False, f"Format de données inattendu: {data}"
                except ValueError as e:
                    print(f"Erreur de décodage JSON: {str(e)}")
                    return False, f"Erreur de décodage JSON: {str(e)}"
            else:
                error_msg = (
                    f"Échec de récupération des commentaires: "
                    f"{response.status_code}"
                )
                return False, error_msg
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def create_comment(self, comment_data, issue_id=None):
        """Crée un nouveau commentaire sur une issue.

        Args:
            comment_data: Données du commentaire (description)
            issue_id: ID de l'issue. Si non spécifié, utilise self.issue_id

        Returns:
            (success, data): Tuple avec booléen de succès et données/message
        """
        if not self.project_id:
            return False, "Aucun projet sélectionné"

        if not issue_id and not self.issue_id:
            return False, "Aucune issue sélectionnée"

        issue_id = issue_id or self.issue_id

        try:
            url = (
                f"{self.api_url}/api/projects/{self.project_id}/issues/"
                f"{issue_id}/comments/"
            )
            response = requests.post(
                url,
                headers=self.get_headers(),
                json=comment_data,
            )

            if response.status_code == 201:
                return True, response.json()
            else:
                error_detail = ""
                try:
                    error_detail = response.json()
                except json.JSONDecodeError:
                    error_detail = response.text

                error_msg = f"Échec de création du commentaire: {error_detail}"
                return False, error_msg
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def token_info(self):
        """Retourne les informations sur le token JWT."""
        if not self.access_token:
            return False, "Pas de token disponible"

        try:
            decoded = jwt.decode(
                self.access_token, options={"verify_signature": False}
            )

            exp_time = None
            time_left = None

            if "exp" in decoded:
                exp_time = datetime.fromtimestamp(decoded["exp"])
                now = datetime.now()
                time_left = exp_time - now

            return True, {
                "decoded": decoded,
                "exp_time": exp_time,
                "time_left": time_left,
            }
        except Exception as e:
            return False, f"Erreur de décodage: {str(e)}"
