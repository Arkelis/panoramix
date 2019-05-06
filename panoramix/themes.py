import glob
import click
import re
import os
import subprocess

from click.exceptions import Exit

from . import panoramix, abort, success, run_process

NAMES = {
    "yaru": "yaru-git"
}

@panoramix.group()
def themes():
    """Utilitaire de gestion de thèmes."""
    click.secho("Je sors ma potion pour gérer les thèmes !\n", bold=True)
    pass

@themes.command()
def list():
    """Liste les thèmes pris en charge."""
    click.secho("Liste des thèmes pris en charge", bold=True, fg="cyan")
    for name in NAMES:
        click.secho(f"- {name.capitalize()}")

@themes.command()
@click.option("-u", "--upgrade", "upgrade", help="Met à jour le thème.", is_flag=True)
@click.argument("name")
def install(upgrade: str, name: str):
    """Installe ou met à jour le thème demandé."""
    if name.lower() in NAMES:
        name = NAMES[name.lower()]
        if upgrade:
            click.secho(f"Mise à jour du paquet {name} avec DNF...", bold=True, fg="cyan")
            run_process(["sudo", "dnf", "upgrade", name])
        else:
            click.secho(f"Installation du paquet {name} avec DNF...", bold=True, fg="cyan")
            run_process(["sudo", "dnf", "install", name])
    success()
