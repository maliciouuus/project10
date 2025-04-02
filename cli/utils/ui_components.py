#!/usr/bin/env python3
"""Composants UI pour l'interface SoftDesk API."""

import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Console pour une sortie améliorée
console = Console()


def clear_screen():
    """Efface l'écran du terminal."""
    os.system("clear" if os.name == "posix" else "cls")


def show_header(title, subtitle="", info=None):
    """Affiche l'en-tête de l'application avec informations optionnelles."""
    clear_screen()

    console.print(
        Panel.fit(f"[bold blue]{title}[/bold blue]", subtitle=subtitle)
    )

    if info:
        for key, value in info.items():
            if value:
                console.print(f"{key}: [blue]{value}[/blue]")


def show_menu(title, options):
    """Affiche un menu avec des options numérotées."""
    console.print(f"\n[bold]{title}[/bold]")

    for i, (option_key, option_text) in enumerate(options.items(), 1):
        console.print(f"{i}. {option_text}")

    return input_choice(
        f"\nVotre choix (1-{len(options)}): ", list(range(1, len(options) + 1))
    )


def show_categories(categories):
    """Affiche un menu avec des catégories."""
    for category, options in categories.items():
        if options:
            console.print(f"\n[bold]{category}:[/bold]")
            for key, text in options.items():
                console.print(f"{key}. {text}")


def input_text(prompt, password=False):
    """Demande un texte à l'utilisateur."""
    return console.input(f"[bold]{prompt}[/bold] ", password=password)


def input_choice(prompt, valid_choices):
    """Demande un choix à l'utilisateur parmi une liste valide."""
    while True:
        try:
            choice = int(console.input(prompt))
            if choice in valid_choices:
                return choice
            console.print("[red]Choix invalide[/red]")
        except ValueError:
            console.print("[red]Veuillez entrer un nombre[/red]")


def input_boolean(prompt):
    """Demande une réponse oui/non à l'utilisateur."""
    return console.input(f"{prompt} (o/n): ").lower() == "o"


def show_message(message, style=""):
    """Affiche un message avec un style spécifique."""
    console.print(f"[{style}]{message}[/{style}]")


def show_success(message):
    """Affiche un message de succès."""
    show_message(message, style="green")


def show_error(message):
    """Affiche un message d'erreur."""
    show_message(message, style="red")


def show_warning(message):
    """Affiche un message d'avertissement."""
    show_message(message, style="yellow")


def show_info(message):
    """Affiche un message informatif."""
    show_message(message, style="blue")


def pause():
    """Pause l'exécution jusqu'à ce que l'utilisateur appuie sur Entrée."""
    input("\nAppuyez sur Entrée pour continuer...")


def show_json(data):
    """Affiche des données JSON formatées."""
    console.print_json(json.dumps(data))


def create_table(columns, title=None):
    """Crée un tableau avec les colonnes spécifiées."""
    table = Table(show_header=True, header_style="bold", title=title)

    for col in columns:
        table.add_column(col)

    return table


def display_table(table):
    """Affiche un tableau."""
    console.print(table)


def text_input_form(fields):
    """Affiche un formulaire avec plusieurs champs texte.

    Args:
        fields: Liste de tuples (label, password, required)

    Returns:
        Dict contenant les valeurs saisies
    """
    result = {}

    for field_name, is_password, is_required in fields:
        while True:
            value = input_text(f"{field_name}:", password=is_password)

            if not value and is_required:
                show_error(f"Le champ {field_name} est obligatoire")
                continue

            result[field_name.lower().replace(" ", "_")] = value
            break

    return result


def option_form(title, options):
    """Affiche un formulaire de sélection d'option.

    Args:
        title: Titre du formulaire
        options: Dict de valeurs {clé: description}

    Returns:
        La clé de l'option sélectionnée
    """
    console.print(f"\n[bold]{title}:[/bold]")

    # Afficher les options
    option_keys = list(options.keys())
    for i, key in enumerate(option_keys, 1):
        console.print(f"{i}. {options[key]}")

    # Demander le choix
    choice = input_choice(
        f"Choisissez une option (1-{len(options)}): ",
        list(range(1, len(options) + 1)),
    )

    # Retourner la clé correspondante
    return option_keys[choice - 1]
