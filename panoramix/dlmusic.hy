#! /usr/bin/env hy

(import argparse
        subprocess
        os
        click
        deemix.app.cli)

(require [hy.contrib.walk [let]])

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
    (if (and (in "deezer.com" url) (in "/track/" url))
      (let [[file-location filename] (fetch-with-deemix url)]
           (convert-to-opus file-location filename url)
           (clean-deezer-file file-location)))))


;; YOUTUBE HANDLER

;; (defn fetch-with-youtube-dl [url])


;; DEEZER HANDLER

(defn fetch-with-deemix [url]
  (print f"Downloading from Deezer...")
  (setv worker (doto (deemix.app.cli.cli None None)
                     (.login)
                     (.downloadLink [url])))
  (as-> (first (. worker qm queueComplete)) it
        (get (. worker qm queueList) it))
        [(first (. it files))
         (.format "{}-{}" 
           (format-metadata (. it artist))
           (format-metadata (. it title)))])

(defn convert-to-opus [file-location filename url]
  (print "Converting and copying in backup songs...")
  (setv track-number (last (.split url "track/"))
        home-dir (.getenv os "HOME")
        opus-location f"{home-dir}/backup-songs/{filename}.opus"
        ffmpeg-result (.run subprocess
                            ["ffmpeg"
                              "-y" 
                              "-i"
                              file-location
                              "-metadata"
                              f"deezertrack={track-number}"
                              "-c:a" 
                              "libopus" 
                              "-b:a"
                              "152k"
                              opus-location]
                            :capture_output True))
  (print f"File converted and copied at {opus-location}."
         "Removing previously downloaded file..."
         :sep "\n"))

(defn clean-deezer-file [file-location]
  (.system os f"rm \"{file-location}\"")
  (print "File removed."
         "Done!"
         :sep "\n"))


;; COMMON

(defn format-metadata [tag]
  (-> (.lower tag)
      (.replace " " "-")
      (.replace "(" "")
      (.replace ")" "")
      (.replace "[" "")
      (.replace "]" "")))
