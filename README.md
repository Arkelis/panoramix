# Panoramix (outil perso)

Il a plein de potions dans son sac.

## Dépendances

* [`click`](https://github.com/pallets/click) : outil pour écrire des programmes en ligne de commande.
* [`hy`](https://github.com/hylang/hy) : Lisp pour Python

## Utilisation

Soit comme un module, dans le dossier contenant Panoramix

`$ python -m panoramix <args>`

## Script point d'entrée

On peut aussi créer un point d'entrée dans un dossier du `PATH`. Un exemple dans [ce dépôt](https://github.com/Arkelis/homescripts).

Il faut rendre ce fichier exécutable avec un `chmod +x panoramix`. On peut maintenant faire depuis n'importe où :

```bash
$ panoramix
Usage: panoramix [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  composer  Utilitaire d'installation/suppresion de Composer (PHP).
  dlmusic   Télécharge un morceau avec youtube-dl ou deemix.
  makedocs  Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST...
  themes    Utilitaire de gestion de thèmes.
  update    Met à jour avec eopkg, met à jour pyenv, poetry.
```

## Roadmap

- [ ] Réécriture en [Hy](https://github.com/hylang/hy)
- [ ] Kickstart script

