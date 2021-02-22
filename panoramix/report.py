import click
import os
import json
import requests
from click.exceptions import Exit

from .utils import abort, success, echo_intro


@click.command()
def report():
    """Rapport de connexion."""

    echo_intro("Nouvelles releases Github")

    # Récupération token Github pour authentificiation
    token = os.getenv("GITHUB_TOKEN")

    # Récupération des tags
    L = [] # liste à afficher

    click.secho("Récupération des données...", fg="cyan", bold=True)
    req = requests.get("https://api.github.com/users/Arkelis/subscriptions", auth=("arkelis", token))
    data = json.loads(req.content.decode())
    print(data)
    for item in data:
        req = requests.get(item["releases_url"].replace("{/id}", ""), auth=("arkelis", token))
        data = json.loads(req.content.decode())
        if data:
            print(data)
            L.append(f"{item['full_name']} : {data[0]['tag_name']}")
        else:
            L.append(f"{item['full_name']} : Pas de nouvelle version.")
    click.echo("\n".join(L))
