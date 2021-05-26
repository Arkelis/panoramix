(import
  click
  [.dlmusic [dlmusic]]
  [.update [update]]
  [.makedocs [makedocs]])

(with-decorator
  (click.group)
  (defn panoramix []
    "Programme Panoramix. Il sait faire plein de choses, surtout des potions."))

(doto panoramix
  (.add-command update)
  (.add-command makedocs)
  (.add-command dlmusic))
  
