import click
from click import exceptions
import subprocess


def abort(msg="Fin du programme."):
    click.secho(msg, fg="red", bold=True)
    raise exceptions.Exit(1)


def success():
    click.secho("Terminé.", fg="green", bold=True)
    raise exceptions.Exit(0)


def run_process(list, msg="Une erreur est survenue ou le programme a été interrompu par l'utilisateur."):
    try:
        code = subprocess.run(list).returncode
        if code:
            abort(msg)
    except Exception as err:
        abort("Erreur : " + str(err))


def echo_intro(msg):
    click.secho(msg, bold=True)

