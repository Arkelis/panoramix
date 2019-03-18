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
    click.secho("Je sors ma potion pour fabriquer la doc !\n", bold=True)
    for path in glob.iglob(folder + "/**/*.tex", recursive=True):
        click.secho(f"Fichier trouvé : {path}", bold=True)
        with open(path, "r") as f:
            tex = f.read()
            click.secho("Recherche des \\paragraph{}...", fg="cyan")
            new_tex = re.sub(
                r"\\paragraph\*?\{(?P<titre>.*?)\}", r"\\textbf{\g<titre>~:}", tex
            )
        if tex != new_tex:
            with open("temp.tex", "w") as f:
                click.secho("Création d'un fichier TeX temporaire...", fg="cyan")
                f.write(new_tex)
            to_convert = "temp.tex"
        else:
            click.secho("Rien à faire !", fg="cyan")
            to_convert = path
        click.secho("Conversion en RST...", fg="yellow")
        subprocess.run(["pandoc", to_convert, "-o", f"{path[:-4]}.rst"])
    click.echo("\nNettoyage du fichier temporaire...")
    subprocess.run(["rm", "temp.tex"])
    click.secho("\nTerminé.\n", bold=True, fg="green")
