# pySpriteWorld

## Disclaimer:
Les graphiques utilisés dans ce projet ont été principalement pris ici:
http://opengameart.org/content/tiny-16-basic
Et du code a été pris ici:
http://programarcadegames.com/index.php

## Introduction

Affiche des sprites a l'ecran et tout et tout.
Pour l'instant les sprites se deplacent de facon discrete, mais le code est prevu pour gerer des deplacements au pixel pres.

On peut par exemple afficher ce genre de map:

![alt tag](https://github.com/yannche/pySpriteWorld/blob/master/Cartes/gardenofdelight.png)

Pour tester ce code, et jouer au clavier, taper

    python main_keyboard.py

Pour voir la demo d'utilisation du ramasseur de laitues, taper

    python exercice_laitues.py

Pour une demo du simulateur de robot, taper

    python exercice_robot_sim.py

Les cartes doivent être construites avec le logiciel Tiled ( http://www.mapeditor.org ) et exportées au format json


## Layers

Dans ces cartes, les sprites sont organisees par Layers.
Par convention, ces layers doivent etre l'une des suivantes:
"bg1","bg2","obstacles","ramassable","joueur","en_hauteur"

Chaque layer a des conventions qui lui sont propres:

  * les layers bg1 et bg2 decrivent le background.
    Le joueur n'a aucune interaction avec le background.
    le layer bg1 est affiche en premier, puis bg2

  * le layer obstacle comporte tous les objets non-deplacables et non-ramassables
    par exemple: un mur ou de l'eau

  * le layer ramassable comporte des objets ramassables par l'instruction "ramasse".
    le joueur doit se trouver dessus. L'instruction "ramasse" n'en ramasse qu'un a la fois.
    les objets ramassables sont reposables devant soi, avec l'instruction "depose"

  * le layer en_hauteur n'interagit pas avec le joueur car est trop haut.
      ex: le haut d'une colonne. Ce layer est affiche en dernier

  * le layer joueur contient le ou les joueurs. Un joueur est considere comme un obstacle pour un autre joueur.

  PS: si possible, chaque objet doit figurer dans un seul layer


   layers supplementaires, pas encore implementes:
   ----------------------------------------------

  * le layer lethal comporte ce qui tue le joueur immediatement (ex: de la lave) et qui ne bouge pas

  * le layer actionable a un effet si on utilise l'instruction 'action'
    ex: une porte, un interrupteur

  * le layer creatures decrit les fantomes, trolls et autres trucs qui gelatineux. Lorsqu'un joueur touche une creature, ca doit declencher un evenement particulier, mais les creatures ne sont pas consideres comme des obstacles.


## Dépendances:
  python 2.7

  pygame
