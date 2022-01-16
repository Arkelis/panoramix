(import subprocess)

(import click)

(import .utils [echo-intro echo-and-run success])



(with-decorator
  (click.command)
  (defn update []
    "Met à jour avec eopkg, met à jour pyenv, poetry."

    (echo-intro "Je sors ma potion pour mettre à jour le système !")
    (echo-and-run
      "-> Mise à jour du système avec eopkg..."
      ["sudo" "eopkg" "upgrade"])
    (echo-and-run
      "-> Nettoyage du cache d'eopkg..."
      ["sudo" "eopkg" "delete-cache"])
    (echo-and-run
      "-> Mise à jour de poetry..."
      ["poetry" "self" "update"])
    (echo-and-run
      "-> Mise à jour de pyenv..."
      ["pyenv" "update"])
    (success)))
