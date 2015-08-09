"""
Global constants
"""

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)

ALL_LAYERS = ["bg1","bg2","obstacles","lethal","ramassable","joueur","en_hauteur"]
ALL_LAYERS_SET = set(ALL_LAYERS)

NON_BG_LAYERS = [l for l in ALL_LAYERS if l not in ["bg1","bg2"]]

"""
    layers de base:
    --------------

    * les layers bg1 et bg2 decrivent le background.
      Le joueur n'a aucune interaction avec le background.
      le layer bg1 est affiche en premier, puis bg2

    * le layer obstacle comporte tous les objets non-deplacables et non-ramassables
      par exemple: un mur ou de l'eau

    * le layer ramassable comporte des objets ramassables par l'instruction "ramasse".
      le joueur doit se trouver dessus. L'instruction "ramasse" n'en ramasse qu'un a la fois.
      les objets ramassables sont reposables devant soi, avec l'instruction "depose"

    * le layer lethal comporte ce qui tue le joueur immediatement (ex: de la lave) et qui ne bouge pas

    * le layer en_hauteur n'interagit pas avec le joueur car est trop haut.
      ex: le haut d'une colonne. Ce layer est affiche en dernier

    PS: si possible, chaque objet doit figurer dans un seul layer


     layers supplementaires, pas encore implementes:
     ----------------------------------------------

    * le layer actionable a un effet si on utilise l'instruction 'action'
      ex: une porte, un interrupteur

    * le layer creatures decrit les fantomes, trolls et autres trucs qui gelatineux

"""
