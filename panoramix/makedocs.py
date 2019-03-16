import click
import re
import os
import sh

from . import panoramix

@panoramix.command()
def makedocs():
    """Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST pour Sphinx."""
    click.echo("Je sors ma potion pour fabriquer la doc !\n")
    with open("/media/donnees/Documents/programmation/python/projets/panoramix/python.tex", "r") as f:
        tex = f.read()
        print("Recherche des \\paragraph{}...")
        new_tex = re.sub(r"\\paragraph\*?\{(?P<titre>.*?)\}", r"\\textbf{\g<titre>~:}", tex)
    if tex != new_tex:
        with open("temp.tex", "w") as f:
            click.echo("Création d'un fichier TeX temporaire...")
            f.write(new_tex)
    else:
        click.echo("Rien à faire !")
    click.echo("Conversion en RST...")
    sh.pandoc("python.tex", o="/media/donnees/Documents/programmation/python/memo/rst/python.rst")
    click.echo("Nettoyage du fichier temporaire...")
    sh.rm("temp.tex")
    click.echo("Terminé.\n")
