import click
import subprocess
from click.exceptions import Exit

@click.group()
def panoramix():
    """Programme Panoramix. Il sait faire plein de choses, surtout des potions."""
    click.secho("\nPANORAMIX\n=========\n", bold=True)

def abort(msg="Fin du programme."):
    click.secho("\n" + msg, fg="red", bold=True)
    raise Exit(1)

def success():
    click.secho("\nTerminé.", fg="green", bold=True)

def run_process(list, msg="Une erreur est survenue ou le programme a été interrompu par l'utilisateur."):
    try:
        code = subprocess.run(list).returncode
        if code:
            abort(msg)
    except Exit:
        raise Exit()
    except Exception as err:
        abort("Erreur : " + str(err))

@panoramix.command()
def update():
    """Met à jour avec DNF, met à jour pyenv, poetry."""

    click.secho("Je sors ma potion pour mettre à jour le système !\n", bold=True)
    click.secho("-> Mise à jour du système avec DNF...", fg="cyan", bold=True)
    subprocess.run(["sudo", "dnf", "upgrade"])
    click.secho("-> Mise à jour de poetry...", fg="cyan", bold=True)
    subprocess.run(["poetry", "self:update"])
    click.secho("-> Mise à jour de pyenv...", fg="cyan", bold=True)
    subprocess.run(["pyenv", "update"])

    return success()

from .makedocs import makedocs
from .themes import themes
from .composer import composer
from .homeconf import homeconf

if __name__ == '__main__':
    panoramix()
