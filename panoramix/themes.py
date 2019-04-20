import glob
import click
import re
import os
import subprocess

from click.exceptions import Exit

from . import panoramix, abort, success

@panoramix.group()
def themes():
    """Utilitaire de gestion de thèmes."""
    pass

@themes.command()
def list():
    """Liste les thèmes pris en charge."""
    click.secho("Liste des thèmes pris en charge", bold=True)
    click.secho("Yaru", fg="cyan")

@themes.command()
@click.option("-v", "--verbose", "verbose", help="Mode verbeux.", is_flag=True)
@click.option("-u", "--upgrade", "upgrade", help="Met à jour le thème.", is_flag=True)
@click.argument("name")
def install(verbose, upgrade, name):
    """Installe ou met à jour le thème demandé."""
    os.chdir("/home/guillaume/.themes")
    if glob.glob(name):
        if not upgrade:
            click.secho("Le thème demandé est déjà installé.", fg="yellow")
            success()
        else:
            os.chdir("/home/guillaume/.themes/" + name)
            click.secho("Mise à jour de {}".format(name), bold=True)
            subprocess.run(["git", "pull"])
            subprocess.run(["meson", "build"])
            os.chdir("/home/guillaume/.themes/" + name + "/build")
            subprocess.run(["ninja"])
            subprocess.run(["sudo", "ninja" , "install"])
            success()
