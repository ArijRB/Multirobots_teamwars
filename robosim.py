"""
Robosim Module
"""

from __future__ import absolute_import, print_function, unicode_literals
from core.gameclass import Game,check_init_game_done,get_game
from core.sprite import MySprite,MovingSprite
from core.spritebuilder import SpriteBuilder
from core import glo
from robosim_player import Turtle,unsafe_throw_rays,throw_rays_for_many_players,telemetre_coords
import pygame
import pygame.draw
from dessinable import *
from math import pi,cos,sin,sqrt
import random


#print("""\n---==[ Fonction disponibles ]==---""")
#print("""init,avance,obstacle,oriente,\ntournegauche,tournedroite,telemetre,\ntelemetre_coords,position,orientation,diametre_robot,taille_terrain\nset_position,obstacle_coords\nline,circle,efface\npenup,pendown,color,frame_skip""")
#print("""=[ Pour l'aide, tapez help(fonction) ]=\n""")



###########################################

game = Game()


def init(_boardname=None,MyTurtleClass=Turtle,screen_width=None,screen_height=None):
    """
    Reinitialise la carte et l'ensemble des parametres
    """
    global player,game
    pygame.quit()

    # Let's define a builder class, using on the MyTurtleClass parameter
    class MySpriteBuilder(SpriteBuilder):
        def basicPlayerFactory(self,tileid=None,x=0.0,y=0.0):
            return MyTurtleClass("joueur",x,y)

    name = _boardname if _boardname else 'robot_obstacles'
    game = Game('Cartes/' + name + '.json', MySpriteBuilder,screen_width=screen_width,screen_height=screen_height)

    #game.fps = 20  # frames per second
    game.mainiteration()
    #player = game.player

    # new attributes
    game.pencolor = glo.RED
    game.usepen = False
    game.frameskip = 0


# Fonctions dans le style non-objet
def position(entiers=False,p=None):                  return (p or game.player).position(entiers)
def avance(t=1.0,p=None):                            return (p or game.player).avance(t)
def tournegauche(a,p=None):                          return (p or game.player).tournegauche(a)
def tournedroite(a,p=None):                          return (p or game.player).tournedroite(a)
def set_position(x,y,p=None):                        return (p or game.player).set_position(x,y)
def oriente(a,p=None):                               return (p or game.player).oriente(a)
def obstacle(s=1.0,p=None):                          return (p or game.player).obstacle(s)
def obstacle_coords(x,y,p=None):                     return (p or game.player).obstacle_coords(x,y)
def telemetre(from_center=False,rel_angle=0,p=None): return (p or game.player).telemetre(from_center,rel_angle)
def orientation(p=None):                             return (p or game.player).orientation()

av, tele, setheading, tg, td, pos, teleporte  = avance, telemetre, oriente, tournegauche, tournedroite, position, set_position
