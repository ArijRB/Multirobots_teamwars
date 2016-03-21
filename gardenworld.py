from __future__ import absolute_import, print_function, unicode_literals
from core.gameclass import Game,check_init_game_done
from core.spritebuilder import SpriteBuilder
from gardenworld_player import GardenPlayer
from core.sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
from core import glo

"""
    Ce fichier est specifique au sprite dans le monde discret (e.g. tiles 32x32),
    Il contient aussi les commandes de base (tournegauche, avance...)
"""


class GardenSpriteBuilder(SpriteBuilder):
    """ classe permettant d'afficher le personnage sous 4 angles differents
    """
    def basicPlayerFactory(self,tileid,x=0.0,y=0.0):
        imglist = [self.sheet[i, j] for i, j in ((10, 0), (8, 0), (9, 0), (11, 0))]
        p = GardenPlayer("joueur", tileid, x, y, imglist)
        if tileid is not None and tileid[0] in [10, 8, 9, 11]:
            p.translate_sprite(0, 0, 90 * [10, 8, 9, 11].index(tileid[0]))
        return p

#############################################################################

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'gardenofdelight'
    game = Game('Cartes/' + name + '.json', GardenSpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    populate_sprite_names(game.O)
    #game.fps = 60  # frames per second
    game.mainiteration()
    player = game.player

def populate_sprite_names(ontology):
    for layer in game.layers.values():
        for s in layer:
            s.firstname = ontology.firstname(s)


@check_init_game_done
def tournegauche(p=None):
    p = player if p is None else p
    p.translate_sprite(0, 0, -90)
    game.mainiteration()

@check_init_game_done
def tournedroite(p=None):
    p = player if p is None else p
    p.translate_sprite(0, 0, 90)
    game.mainiteration()

@check_init_game_done
def avance(p=None):
    p = player if p is None else p
    p.forward(p.rect.width,check_collision_and_update=game.mask.check_collision_and_update)
    game.mainiteration()
    return p.position_changed()



@check_init_game_done
def ramasse(p=None):
    p = player if p is None else p
    o = p.ramasse(game.layers)
    game.mainiteration()
    return game.O.firstname(o)

@check_init_game_done
def obstacle(p=None):
    p = player if p is None else p
    p.forward(p.rect.width)
    hors = game.mask.out_of_screen(p)
    coll = game.mask.collision_blocking_player(p)
    p._resume_to_backup()
    return hors or coll != []

@check_init_game_done
def depose(nom=None,p=None):
    def _filtre(o): return nom in game.O.names(o) + [None]

    p = player if p is None else p
    o = p.depose(game.layers, _filtre)
    game.mainiteration()
    return game.O.firstname(o)

@check_init_game_done
def cherche(nom=None,p=None):
    def _filtre(o): return nom in game.O.names(o) + [None]

    p = player if p is None else p
    o = p.cherche_ramassable(game.layers, _filtre)
    game.mainiteration()
    return game.O.firstname(o)


tg, td, av, ra, dp, ch, reset, ob = tournegauche, tournedroite, avance, ramasse, depose, cherche, init, obstacle
