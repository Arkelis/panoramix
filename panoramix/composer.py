import click
import requests
import hashlib
import os

from .utils import success, run_process, abort, echo_intro


home_dir = os.getenv("HOME")

@click.group()
def composer():
    """Utilitaire d'installation/suppresion de Composer (PHP)."""
    pass


@composer.command()
def install():
    """Installe composer."""
    echo_intro("Je sors ma potion pour installer Composer !")
    click.secho("Téléchargement de l'installateur...", bold=True, fg="cyan")
    run_process(["php", "-r", "copy('https://getcomposer.org/installer', 'composer-setup.php');"])
    click.secho("Véfification du téléchargement...", bold=True, fg="cyan")
    downloaded_sig = hashlib.sha384(open("composer-setup.php").read().encode()).hexdigest()
    trusted_sig = requests.get("https://composer.github.io/installer.sig").text.replace("\n", "")
    if downloaded_sig == trusted_sig:
        click.secho("Vérifié !")
    else:
        abort("Les signatures sont différentes.")
    click.secho(f"Création de l'exécutable de composer dans {home_dir}/.local/bin...", bold=True, fg="cyan")
    run_process(["php", "composer-setup.php", "--install-dir", f"{home_dir}/.local/bin", "--filename", "composer"])
    click.secho("Nettoyage...", bold=True, fg="cyan")
    run_process(["php", "-r", "unlink('composer-setup.php');"])
    success()


@composer.command()
def uninstall():
    "Supprime composer."
    echo_intro("Je sors ma potion pour supprimer Composer !")
    click.secho("Suppression de composer...", bold=True, fg="cyan")
    run_process(["sudo", "rm", f"{home_dir}/.local/bin/composer"])
    success()
