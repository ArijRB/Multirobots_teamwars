from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo
import time
"""
    Ce fichier est specifique au sprite dans le monde discret (e.g. tiles 32x32),
    Il contient aussi les commandes de base (tournegauche, avance...)
"""


class GardenSpriteBuilder(SpriteBuilder):
    """ classe permettant d'afficher le personnage sous 4 angles differents
    """
    def basicSpriteFactory(self, layername, tileid, x, y, img=None):
        if img is None: img = self.sheet[tileid]
        if layername == "joueur":
            imglist = [img]
            p = Player(layername, tileid, x, y, imglist)
            if tileid[0] in [10, 8, 9, 11]:
                p.translate_sprite(0, 0, 90 * [10, 8, 9, 11].index(tileid[0]))
            return p
        elif layername == "personnage":
            return MovingSprite(layername, tileid, x, y, [img])
        else:
            return SpriteBuilder.basicSpriteFactory(self, layername, tileid, x, y, img)


#############################################################################

game = Game()
init_x , init_y = None,None

def init(_boardname='canon'):
    global player,game,init_x,init_y
    name = _boardname if _boardname is not None else 'gardenofdelight'
    game = Game('Cartes/' + name + '.json', GardenSpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 60  # frames per second

    player = game.player
    init_x,init_y = player.x , player.y
    player.translate_sprite(-200,0,0)
    player.backup()
    game.mainiteration()

@check_init_game_done
def frameskip(n):
    """
    frameskip(n) n'affichera qu'une image sur n.
    frameskip(0) affiche tout, et donc c'est assez lent.
    """
    game.frameskip = n



def tir(_vy=0.1,_vx=3.0):
    global init_x,init_y
    t = time.time()
    player.translate_sprite(init_x,init_y,0,relative=False)
    player.backup()
    game.mainiteration()


    sprite_but = list( game.layers['obstacle'])[0]
    but_x = sprite_but.rect.x + sprite_but.rect.w/2.0
    vx = _vx
    vy = -_vy
    while True:
        player.translate_sprite(vx, vy, 0)
        vy += 0.1
        hors = game.mask.out_of_screen(player)
        coll = game.mask.get_box_collision_list(chain(game.layers['obstacle'],game.layers['personnage']), player)
        game.mainiteration()
        if hors:
            return player.dist( sprite_but.rect.x+sprite_but.rect.w/2.0 ,   sprite_but.rect.y+sprite_but.rect.h/2.0)
        if coll:
            return 0.0


@check_init_game_done
def tournegauche():
    player.translate_sprite(0, 0, -90)
    game.mainiteration()

@check_init_game_done
def tournedroite():
    player.translate_sprite(0, 0, 90)
    game.mainiteration()

@check_init_game_done
def avance():
    player.forward(player.rect.width)
    game.mainiteration()
    return player.position_changed()

@check_init_game_done
def ramasse():
    o = game.player.ramasse(game.layers)
    game.mainiteration()
    return game.O.firstname(o)

@check_init_game_done
def obstacle():
    player.forward(player.rect.width)
    hors = game.mask.out_of_screen(player)
    coll = game.mask.get_box_collision_list(chain(game.layers['obstacle'],game.layers['personnage']), player)
    player.resume_to_backup()
    return hors or coll != []

@check_init_game_done
def depose(nom=None):
    def _filtre(o): return nom in game.O.names(o) + [None]

    o = player.depose(game.layers, _filtre)
    game.mainiteration()
    return game.O.firstname(o)

@check_init_game_done
def cherche(nom=None):
    def _filtre(o): return nom in game.O.names(o) + [None]

    o = player.cherche_ramassable(game.layers, _filtre)
    game.mainiteration()
    return game.O.firstname(o)


tg, td, av, ra, dp, ch, reset, ob = tournegauche, tournedroite, avance, ramasse, depose, cherche, init, obstacle
