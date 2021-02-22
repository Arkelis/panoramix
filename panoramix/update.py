import click

@click.command()
def update():
    """Met à jour avec eopkg, met à jour pyenv, poetry."""

    echo_intro("Je sors ma potion pour mettre à jour le système !")
    click.secho("-> Mise à jour du système avec eopkg...", fg="cyan", bold=True)
    subprocess.run(["sudo", "eopkg", "upgrade"])
    click.secho("-> Nettoyage du cache d'eopkg...", fg="cyan", bold=True)
    subprocess.run(["sudo", "eopkg", "delete-cache"])
    click.secho("-> Mise à jour de poetry...", fg="cyan", bold=True)
    subprocess.run(["pipx", "upgrade", "poetry"])
    click.secho("-> Mise à jour de pyenv...", fg="cyan", bold=True)
    subprocess.run(["pyenv", "update"])

    return success()
