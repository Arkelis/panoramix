import glob
import click
import re
import os
import subprocess

from click.exceptions import Exit

from .utils import abort, success, echo_intro
    

@click.command()
@click.option("-v", "--verbose", "verbose", help="Mode verbeux.", is_flag=True)
def makedocs(verbose):
    """Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST pour Sphinx.
    
    Cherche un fichier .tex dans le répertoire courant. S'il y en a un, effectue une
    recherche récursive te fichiers .tex et les convertit tous en fichiers .rst et les 
    place dans le dossier ../rst/.
    """
    echo_intro("Je sors ma potion pour fabriquer la doc !")
    click.secho("Conversion des fichers .tex en .rst...\n", bold=True, fg="cyan")
    try:
        from .settings import makedocs_settings 
    except (NameError, ModuleNotFoundError):
        click.secho("Fichier de configuration non trouvé. Paramètres par défaut.", fg="yellow")
        from .settings import makedocs_settings
    if not glob.glob("*.tex"):
        click.secho("Pas de fichier tex dans le dossier courant.", fg="red", bold=True)
        return abort()
    for path in glob.iglob("*/*.tex", recursive=True):
        click.secho(f"Fichier trouvé : {path}", bold=True)
        with open(path, "r") as f:
            tex = f.read()
            if verbose:
                click.secho("Application des modifications nécessaires...", fg="cyan")
            for t in makedocs_settings["subs"]:
                new_tex = re.sub(*t, tex)
        if tex != new_tex:
            with open("temp.tex", "w") as f:
                if verbose:
                    click.secho("Création d'un fichier TeX temporaire avec les modifications...", fg="cyan")
                f.write(new_tex)
            to_convert = "temp.tex"
        else:
            if verbose:
                click.secho("Rien à faire !", fg="cyan")
            to_convert = path
        if verbose:
            click.secho("Conversion en RST...", fg="yellow")
        subprocess.run(["pandoc", to_convert, "-o", f"../rst/{path[:-4]}.rst"])
    click.secho("\nConversion terminée ! Compilation avec sphinx...\n", bold=True, fg='cyan')
    subprocess.run(["make", "html"], cwd="../rst")
    click.echo("\nNettoyage du fichier temporaire...")
    subprocess.run(["rm", "temp.tex"])
    return success()
