#! /usr/bin/env hy

(import subprocess
        os
        click
        deemix.app.cli
        youtube-dl)

(import [panoramix [utils]])

;; entry point command

(with-decorator
  (click.command)
  (click.argument "url")
  (defn dlmusic [url]
    "Télécharge un morceau avec youtube-dl ou deemix.
    
    Télécharge la musique à URL et sauvegarde au format opus.
    URL peut être une chanson de Youtube (téléchargée par youtube-dl) ou de
    Deezer (téléchargée par deemix). Le fichier est ensuite converti au format
    opus avec ffmpeg.
    "
    (utils.echo-intro "Je sors ma potion télécharger de la musique !")
    (if 
      (and (in "deezer.com" url) (in "/track/" url))
        (-> (unpack-iterable (fetch-with-deemix url))
            (convert-deezer-to-opus)
            (clean-file))
      (in "youtu" url)
        (fetch-with-youtube-dl url))))


;; YOUTUBE HANDLER

(defn fetch-with-youtube-dl [url]
  (print f"Téléchargement depuis Youtube...")
  (doto (youtube-dl.YoutubeDL {"format" "251"
                               "progress_hooks" [convert-yt-to-opus]})
        (.download [url])))

(defn convert-yt-to-opus [data]
  (if (= (get data "status") "finished")
    (do
      (setv yt-location (get data "filename")
            artist (input "Artiste : ")
            title (input "Titre : ")
            album (input "Album : ")
            filename (.format "{}-{}" 
                        (format-metadata artist)
                        (format-metadata title))
            home-dir (.getenv os "HOME")
            opus-location f"{home-dir}/backup-songs/{filename}.opus")
      (print "Ajout des métadonnées et copie dans backup-songs...")
      (subprocess.run ["ffmpeg"
                       "-y" 
                       "-i"
                       yt-location
                       "-metadata"
                       f"artist={artist}"
                       "-metadata"
                       f"title={title}"
                       "-metadata"
                       f"album={album}"
                       "-c:a" 
                       "copy" 
                       opus-location])
      (print f"Fichier converti et copié à {opus-location}."
             "Suppression du fichier précédemment téléchargé..."
             :sep "\n")
      (clean-file yt-location))))


;; DEEZER HANDLER

(defn fetch-with-deemix [url]
  (print "Téléchargement depuis Deezer...")
  (setv worker (doto (deemix.app.cli.cli None None)
                     (.login)
                     (.downloadLink [url])))
  (as-> (first (. worker qm queueComplete)) it
        (get (. worker qm queueList) it))
        [(first (. it files))
         (.format "{}-{}" 
           (format-metadata (. it artist))
           (format-metadata (. it title)))
         url])

(defn convert-deezer-to-opus [file-location filename url]
  (print "Conversion et copie dans backup-songs...")
  (setv track-number (last (.split url "track/"))
        home-dir (.getenv os "HOME")
        opus-location f"{home-dir}/backup-songs/{filename}.opus"
        ffmpeg-result (subprocess.run ["ffmpeg" "-y"  "-i" file-location
                                       "-metadata" f"deezertrack={track-number}"
                                       "-c:a" "libopus" 
                                       "-b:a" "152k"
                                       "-af" "silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-50dB"
                                       opus-location]))
  (print f"Fichier converti et copié à {opus-location}."
         "Suppression du fichier précédemment téléchargé..."
         :sep "\n")
  file-location)


;; COMMON

(defn format-metadata [tag]
  (-> (.lower tag)
      (.replace " " "-")
      (.replace "(" "")
      (.replace ")" "")
      (.replace "[" "")
      (.replace "]" "")))

(defn clean-file [file-location]
  (.system os f"rm \"{file-location}\"")
  (print "Fichier supprimé."
         "Terminé !"
         :sep "\n"))
