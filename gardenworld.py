from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

"""
    Ce fichier est specifique au sprite dans le monde discret (e.g. tiles 32x32),
    Il contient aussi les commandes de base (tournegauche, avance...)
"""


class GardenSpriteBuilder(SpriteBuilder):
    """ classe permettant d'afficher le personnage sous 4 angles differents
    """
    def basicSpriteFactory(self,spritegroups, layername, tileid, x, y, img=None):
        if img is None: img = self.sheet[tileid]
        if layername == "joueur":
            imglist = [self.sheet[i, j] for i, j in ((10, 0), (8, 0), (9, 0), (11, 0))]
            p = Player(layername, tileid, x, y, imglist)
            if tileid[0] in [10, 8, 9, 11]:
                p.translate_sprite(0, 0, 90 * [10, 8, 9, 11].index(tileid[0]))
            spritegroups[layername].add(p)
        elif layername == "personnage":

            p = MovingSprite(layername, tileid, x, y, [img])
            spritegroups[layername].add(p)
        else:
            SpriteBuilder.basicSpriteFactory(self,spritegroups, layername, tileid, x, y, img)


#############################################################################

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'gardenofdelight'
    game = Game('Cartes/' + name + '.json', GardenSpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.fps = 60  # frames per second
    game.mainiteration()
    player = game.player



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
