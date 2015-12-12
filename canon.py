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
from robosim import frameskip,tournegauche,tournedroite,avance,obstacle,init as init_robosim

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
player , init_x , init_y = None,None,None

def init(_boardname='canon'):
    global player,game,init_x,init_y
    init_robosim('canon',GardenSpriteBuilder)
    game.fps = 60  # frames per second
    player = game.player
    init_x,init_y = player.x , player.y
    player.remove( game.layers['joueur'] )
    game.mainiteration()



def tir(_vy=0.1,_vx=3.0):
    global init_x,init_y
    t = time.time()
    game.layers['joueur'].add( player )
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
