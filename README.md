# Panoramix (outil perso)

Il a plein de potions dans son sac.

## Dépendances

* [`click`](https://github.com/pallets/click) : outil pour écrire des programmes en ligne de commande.

## Utilisation

Soit comme un module, dans le dossier contenant Panoramix

`$ python -m panoramix <args>`

Soit en créant un petit script Python faisant office d'exécutable dans votre dossier `~/.local/bin`.
Ce fichier nommé par exemple `panoramix` devrait contenir par exemple :

```python3
#!/usr/bin/env python3

import re
import sys

sys.path.append(<chemin vers le dossier panoramix>) # nécessaire car on ne place pas panoramix dans site-packages

from panoramix import panoramix

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(panoramix())
```

Il faut rendre ce fichier exécutable avec un `chmod +x panoramix`. On peut maintenant faire depuis n'importe où :

```bash
$ panoramix
Usage: panoramix [OPTIONS] COMMAND [ARGS]...

  Programme Panoramix. Il sait faire plein de choses, surtout des potions.

Options:
  --help  Show this message and exit.

Commands:
  makedocs  Utilitaire pour convertir le Mémo Python LaTeX en fichiers RST...
```

## Commandes

* `makedocs` : outil pour convertir le [mémo Python en TeX](https://github.com/arkelis/memo-python) vers le format RST
  pour générer [la version Web](https://www.pycolore.fr/python/).
