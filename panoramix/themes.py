import glob
import pathlib

import click
import re
import os
import subprocess

from click.exceptions import Exit

from .utils import abort, success, run_process, echo_intro


NAMES = {}


@click.group()
def themes():
    """Utilitaire de gestion de thèmes."""
    echo_intro("Je sors ma potion pour gérer les thèmes !")
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
            click.secho(f"Mise à jour du paquet {name} avec eopkg...", bold=True, fg="cyan")
            run_process(["sudo", "eopkg", "upgrade", name])
        else:
            click.secho(f"Installation du paquet {name} avec eopkg...", bold=True, fg="cyan")
            run_process(["sudo", "eopkg", "install", name])
    elif name == "qogir":
        click.secho("Installation / Mise à jour du thème Qogir")
        themes_dir = pathlib.Path("")
    success()
