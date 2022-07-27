#! /usr/bin/env hy

(require hyrule [-> as-> doto])

(import subprocess
        shutil
        os
        pathlib [Path])

(import click
        deemix.__main__ :as deemix
        mutagen.id3 [ID3]
        youtube-dl
        toolz [first last])

(import panoramix [utils])

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
    (utils.echo-intro "Je sors ma potion pour télécharger de la musique !")
    (cond 
      [(and (in "deezer.com" url) (in "/track/" url))
        (-> (unpack-mapping (fetch-with-deemix url))
            (convert-deezer-to-opus)
            (clean-file))]
      [(in "youtu" url)
        (fetch-with-youtube-dl url)]
      [(in "qobuz" url)
        (fetch-with-qobuz-dl url)])))



;; QOBUZ HANDLER

(setv QOBUZ-TMP-DIR "/tmp/qobuz")

(defn fetch-with-qobuz-dl [url]
  (subprocess.run ["qobuz-dl" "dl" "--no-db" url])
  (convert-qobuz-to-opus url))

(defn get-opus-and-thumbnail [path url]
  (let 
    [music-filename (-> (path.glob "*.mp3") (first) (.resolve))
     music-file (ID3 music-filename)
     cover-filename (-> (path.glob "*.jpg") (first) (.resolve))
     track-number (last (.split url "track/"))
     filename
      (.format "{}-{}" 
        (format-metadata (extract-metadata "artist" music-file))
        (format-metadata (extract-metadata "title" music-file)))
     home-dir (.getenv os "HOME")
     opus-location f"{home-dir}/Musique/pycolore/{filename}.opus"
     cover-location f"{home-dir}/Musique/pycolore/{filename}.jpg"]
    (shutil.move cover-filename cover-location)
    (convert-to-opus music-filename opus-location f"q-{track-number}")))

(defn convert-qobuz-to-opus [url]
  (as-> (Path QOBUZ-TMP-DIR) it
        (it.glob "*")
        (filter (fn [x] (x.is-dir)) it)
        (for [path it]
          (get-opus-and-thumbnail path url)
          (shutil.rmtree path))))

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
            opus-location f"{home-dir}/Musique/pycolore/{filename}.opus")
      (print "Ajout des métadonnées et copie dans backup-songs...")
      (subprocess.run ["ffmpeg" "-y" "-i" yt-location
                       "-metadata" f"artist={artist}"
                       "-metadata" f"title={title}"
                       "-metadata" f"album={album}"
                       "-c:a" 
                       "copy" 
                       opus-location])
      (print f"Fichier converti et copié à {opus-location}."
             "Suppression du fichier précédemment téléchargé..."
             :sep "\n")
      (clean-file yt-location))))


;; DEEZER HANDLER

(setv DEEMIX-TMP-DIR "/tmp/deemix")


(defn extract-metadata [name mutagen-file]
  (let [metamap {"title" "TIT2"  "artist" "TPE1"}
        metaname (get metamap name)]
    (-> mutagen-file (.get metaname) (. text) (first))))


(defn fetch-with-deemix [url]
  (print "Téléchargement depuis Deezer...")
  (.system os f"deemix {url} --path {DEEMIX-TMP-DIR}")
  (as-> (Path DEEMIX-TMP-DIR) it
        (.glob it "*.mp3")
        (first it)
        {"file_location" (.resolve it)
         "filename" 
           (let [file (ID3 (.resolve it))]
             (.format "{}-{}" 
               (format-metadata (extract-metadata "artist" file))
               (format-metadata (extract-metadata "title" file))))
         "url" url}))

(defn convert-deezer-to-opus [file-location filename url]
  (print "Conversion et copie dans backup-songs...")
  (setv track-number (last (.split url "track/"))
        home-dir (.getenv os "HOME")
        opus-location f"{home-dir}/Musique/pycolore/{filename}.opus"
        ffmpeg-result (convert-to-opus file-location opus-location track-number))
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
  (.system os f"rm '{file-location}'")
  (print "Fichier supprimé."
         "Terminé !"
         :sep "\n"))

(defn convert-to-opus [input-filename output-filename [track-number None]]
  (subprocess.run ["ffmpeg" "-y"  "-i" input-filename
                   #* (if track-number ["-metadata" f"trackid={track-number}"] [])
                   "-c:a" "libopus" 
                   "-b:a" "152k"
                   "-af" "silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-50dB"
                   output-filename]))