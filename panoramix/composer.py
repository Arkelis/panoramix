import click
import subprocess
import requests
import hashlib

from . import panoramix, success, run_process, abort

@panoramix.group()
def composer():
    """Utilitaire de gestion de thèmes."""
    pass

@composer.command()
def install():
    """Installe composer."""
    click.secho("Je sors ma potion pour installer Composer !\n", bold=True)
    click.secho("Téléchargement de l'installateur...", bold=True, fg="cyan")
    run_process(["php", "-r", "copy('https://getcomposer.org/installer', 'composer-setup.php');"])
    click.secho("Véfification du téléchargement...", bold=True, fg="cyan")
    downloaded_sig = hashlib.sha384(open("composer-setup.php").read().encode()).hexdigest()
    trusted_sig = requests.get("https://composer.github.io/installer.sig").text.replace("\n", "")
    if downloaded_sig == trusted_sig:
        click.secho("Vérifié !")
    else:
        abort("Les signatures sont différentes.")
    click.secho("Génération de composer...", bold=True, fg="cyan")
    run_process(["sudo", "php", "composer-setup.php", "--install-dir", "/usr/bin", "--filename", "composer"])
    click.secho("Nettoyage...", bold=True, fg="cyan")
    run_process(["php", "-r", "unlink('composer-setup.php');"])
    success()

@composer.command()
def uninstall():
    "Supprime composer."
    click.secho("Je sors ma potion pour supprimer Composer !\n", bold=True)
    click.secho("Suppression de composer...", bold=True, fg="cyan")
    run_process(["sudo", "rm", "/usr/bin/composer"])
    success()
