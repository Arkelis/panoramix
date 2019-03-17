import glob
import click
import re
import os
import subprocess

from . import panoramix

@panoramix.command()
@click.argument("folder")
def makedocs(folder):
    """Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST pour Sphinx."""
    click.echo("Je sors ma potion pour fabriquer la doc !\n")
    for path in glob.iglob(folder + "/**/*.tex", recursive=True):
        print(path)
        with open(path, "r") as f:
            tex = f.read()
            print("Recherche des \\paragraph{}...")
            new_tex = re.sub(r"\\paragraph\*?\{(?P<titre>.*?)\}", r"\\textbf{\g<titre>~:}", tex)
        if tex != new_tex:
            with open("temp.tex", "w") as f:
                click.echo("Création d'un fichier TeX temporaire...")
                f.write(new_tex)
                to_convert = "temp.tex"
        else:
            click.echo("Rien à faire !")
            to_convert = path
        click.echo("Conversion en RST...")
        sh.pandoc(to_convert, o=path[:-4] + ".rst")
    click.echo("Nettoyage du fichier temporaire...")
    sh.rm("temp.tex")
    click.echo("Terminé.\n")
