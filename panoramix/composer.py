import glob
import click
import re
import os
import subprocess

from . import panoramix, success, run_process

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
    run_process(["php", "-r", "if (hash_file('sha384', 'composer-setup.php') === '48e3236262b34d30969dca3c37281b3b4bbe3221bda826ac6a9a62d6444cdb0dcd0615698a5cbe587c3f0fe57a54d8f5') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"])
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
