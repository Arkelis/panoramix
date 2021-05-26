(import subprocess
        click
        [click [exceptions]])


(defn abort [[msg "Fin du programme"]]
  (click.secho msg :fg "red" :bold True)
  (raise (exceptions.Exit 1)))

(defn success []
  (click.secho "Terminé." :fg "green" :bold True)
  (raise (exceptions.Exit 1)))

(defn run-process [list 
                   [msg "Une erreur est survenue ou le programme a été interrompu par l'utilisateur"]]
;;   (try
  (if (. (subprocess.run list) returncode)
    (abort msg)))
;;   (except [err Exception]
;;     (abort f"Erreur : {err}"))))

(defn echo-and-run [msg command]
  (click.secho msg :fg "cyan" :bold True)
  (run-process command))

(defn echo-intro [msg]
    (click.secho msg :bold True))

