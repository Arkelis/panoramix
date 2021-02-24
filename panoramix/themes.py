import glob
import os
import pathlib
import re
import subprocess
import shutil

import click
from click.exceptions import Exit

from .utils import abort, echo_intro, run_process, success

HOME = os.getenv("HOME")
NAMES = {"Qogir": ""}


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
@click.option("-u",
              "--upgrade",
              "upgrade",
              help="Met à jour le thème.",
              is_flag=True)
@click.argument("name")
def install(upgrade: str, name: str):
    """Installe ou met à jour le thème demandé."""
    if name.lower() in NAMES:
        name = NAMES[name.lower()]
        if upgrade:
            click.secho(f"Mise à jour du paquet {name} avec eopkg...",
                        bold=True,
                        fg="cyan")
            run_process(["sudo", "eopkg", "upgrade", name])
        else:
            click.secho(f"Installation du paquet {name} avec eopkg...",
                        bold=True,
                        fg="cyan")
            run_process(["sudo", "eopkg", "install", name])
    elif name == "qogir":
        click.secho("Installation / Mise à jour du thème Qogir")
        themes_dir = pathlib.Path(f"{HOME}/.themes")
        qogir_dir = themes_dir / pathlib.Path("Qogir-theme")
        if not qogir_dir.is_dir():
            subprocess.run(["git", "clone", "https://github.com/vinceliuice/Qogir-theme/", str(qogir_dir)])
        os.chdir(qogir_dir)
        subprocess.run(["git", "pull"])
        subprocess.run(["./install.sh"])
    success()


@themes.command()
@click.argument("name")
def uninstall(name: str):
    """Supprime le thème demandé."""
    if name == "qogir":
        click.secho("Suppression du thème Qogir")
        themes_dir = pathlib.Path(f"{HOME}/.themes")
        qogir_dir = themes_dir / pathlib.Path("Qogir-theme")
        if not qogir_dir.is_dir():
            abort("Le thème Qobir n'est pas installé.")
        for p in themes_dir.glob("Qogir*/"):
            shutil.rmtree(p, ignore_errors=True)
    else:
        abort("Thème non installé")
    success()

