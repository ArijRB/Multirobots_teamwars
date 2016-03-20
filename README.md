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


Pour voir la demo d'utilisation du ramasseur de laitues, taper

    python -m Tests.exercice_laitues

Pour une demo du simulateur de robot, taper

    python -m Tests.exercice_robot_sim


Les cartes doivent être construites avec le logiciel Tiled ( http://www.mapeditor.org ) et exportées au format json


## Layers

Dans ces cartes, les sprites sont organisees par Layers.
Par convention, ces layers doivent etre l'une des suivantes:
"bg1","bg2","obstacle","ramassable","joueur"

Chaque layer a des conventions qui lui sont propres:

  * les layers bg1 et bg2 decrivent le background.
    Le joueur n'a aucune interaction avec le background.
    le layer bg1 est affiche en premier, puis bg2

  * le layer obstacle comporte tous les objets non-deplacables et non-ramassables et infranchissables
    par exemple: un mur ou de l'eau

  * le layer ramassable comporte des objets ramassables par l'instruction "ramasse".
    le joueur doit se trouver dessus. L'instruction "ramasse" n'en ramasse qu'un a la fois.
    les objets ramassables sont reposables devant soi, avec l'instruction "depose"

  * le layer joueur contient le ou les joueurs. Un joueur est considere comme un obstacle pour un autre joueur.

  PS: si possible, chaque objet doit figurer dans un seul layer



## Dépendances:
  python version 2.7 -> version 3.5

  pygame
