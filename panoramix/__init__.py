# This is Panoramix, PostTexRST to FinalRST converter for PyColore. This simply
# does some processing after pandoc converts Tex files to RST.

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

def run_process(list, msg="Une erreur est survenue."):
    try:
        code = subprocess.run(list).returncode
        if code:
            abort(msg)
    except Exception as err:
        abort("Erreur : " + str(err))

from .makedocs import makedocs
from .themes import themes
from .composer import composer

if __name__ == '__main__':
    panoramix()
