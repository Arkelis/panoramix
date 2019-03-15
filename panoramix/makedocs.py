import click

from . import panoramix

@panoramix.command()
def makedocs():
    """Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST pour Sphinx."""
    click.echo("Je fabrique la doc...")