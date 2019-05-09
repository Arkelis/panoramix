import click
import subprocess
import os
import glob
import itertools
from datetime import date

from . import panoramix, success, abort
from .settings import homeconf_settings as settings

DEVNULL = open(os.devnull, 'w')

HOME = os.path.expanduser("~")

GIT_PATH = os.path.join(HOME, "Documents/homeconf-git")


@panoramix.group()
def homeconf():
    """Utilitaire pour synchroniser les fichiers de configuration utilisateur.
    
    L'outil stocke les fichiers voulus dans ~/Documents/homeconf-git/, en fait
    un dépôt git et les push sur le dépôt distant voulu (demandé lors du premier
    push).
    """
    
    click.secho("Je sors ma potion pour gérer la config home !\n", bold=True)

@homeconf.command()
def push():
    """Téléverse les fichiers de configuration actuels sur le dépôt distant.
    
    Si le dépôt n'existe pas, il faut fournir une URL pour le dépôt distant.
    Les fichiers sont remplacés par des liens symboliques pointant vers le dépôt
    local. Si des changements sont détectés, ils sont commités et poussés sur le 
    dépôt. Le message de commit a pour forme :

        [Panoramix] Saving files on AAAA-MM-JJ

    """
    
    click.secho("Sauvegarde de la configuration locale sur le dépôt distant...", bold=True, fg="cyan")
    
    # Création du dossier si nécessaire
    created = create_directory_or_pass()
    
    # Création du dépôt git
    if created:
        click.secho("Initialisation du dépôt Git...", bold=True, fg="cyan")
        subprocess.run(["git", "init"])
    

    # Copie des fichiers
    for file in settings["files"]:
        if not glob.glob(file):
            click.secho(f"Copie du fichier {file}", fg="cyan")
            os.rename(str(HOME) + "/" + file, file)
            os.symlink(str(GIT_PATH) + "/" + file, str(HOME) + "/" + file)

    # Commit
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"[Panoramix] Saving files on {date.today().isoformat()}"])

    # Push
    git_push = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = git_push.communicate()
    print((std_out or std_err).decode())
    if git_push.returncode:
        if "git remote add" in std_err.decode():
            remote_url = input("Entrer l'URL du dépôt git où vous souhaitez stocker vos fichiers de conf : ")
            subprocess.run(["git", "remote", "add", "origin", remote_url])
            subprocess.run(["git", "push", "-u", "origin", "master"])
        elif "Could not resolve hostname github.com" in std_err.decode():
            abort("Vérifier la connexion internet.")
        else:
            abort("Erreur git non prise en charge.")
    success()

@homeconf.command()
def pull():
    """Télécharge les fichiers de configuration du dépôt distant.

    Si le dépôt local n'existe pas, l'URL du dépôt distant à cloner sera demandée.
    Les fichiers de configuration n'étant pas des liens symboliques sont remplacés
    par des liens symbolique. Une copie de sauvegarde est gardée sous la forme
    fichier.bak.
    """

    click.secho("Sauvegarde de la configuration distante sur la machine locale...", bold=True, fg="cyan")

    # Création du dossier si nécessaire
    created = create_directory_or_pass()

    if created:
        remote_url = input("Entrer l'URL du dépôt git d'où vous souhaitez tirer vos fichiers de conf : ")
        subprocess.run(["git", "clone", remote_url, "."])
    else:
        subprocess.run(["git", "pull"])
    
    # on récupère les fichiers du dépôt
    files_in_repo = itertools.chain(glob.iglob(".*"), glob.iglob("*")) # recherche tous les fichiers sauf ".git".
    for file in files_in_repo:
        if file in settings["files"]:
            if not os.path.islink(str(HOME) + "/" + file):
                if os.path.isfile(str(HOME) + "/" + file):
                    click.secho(f"Sauvegarde de {file} dans {file}.bak...", fg="cyan")
                    os.rename(f"{HOME}/{file}", f"{HOME}/{file}.bak")
                click.secho(f"Création du lien symbolique pour {file}...", fg="cyan")
                os.symlink(str(GIT_PATH) + "/" + file, str(HOME) + "/" + file)
            else:
                click.secho(f"Lien symbolique trouvé pour {file}. Vérifier qu'il point bien vers le fichier voulu.", fg="cyan")

    success()

@homeconf.command()
@click.pass_context
def sync(ctx):
    """Effectue un pull puis un push."""
    ctx.invoke(pull)
    ctx.invoke(push)

def create_directory_or_pass():
    """Crée un dépôt git local contenant les fichiers de config si nécessaire.
    
    Les fichiers de config de ~ sont remplacés par des symlinks vers le dépôt git.
    Si rien à faire, ne fait que changer de dossier courant (on se place dans le
    dépôt pour lancer les commandes git.)
    """
    
    # Création du dossier de sauvegarde
    created = False
    if not os.path.isdir(GIT_PATH):
        click.secho("Création du dossier qui contiendra les fichiers de config...", bold=True, fg="cyan")
        os.mkdir(GIT_PATH)
        created = True
    os.chdir(GIT_PATH)
    return created

