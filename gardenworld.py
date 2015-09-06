from gameclass import Game
from spritebuilder import SpriteBuilder
from players import Player
from ontology import Ontology
import pygame


"""
    Ce fichier est specifique au sprite dans le monde discret (e.g. tiles 32x32),
    Il contient aussi les commandes de base (tournegauche, avance...)
"""


class GardenSpriteBuilder(SpriteBuilder):
    """ classe permettant d'afficher le personnage sous 4 angles differents
    """
    def basicSpriteFactory(self,spritegroups , layername,tileid,x,y,img):
        if layername == "joueur":
            imglist = [ self.sheet[i,j] for i,j in ((10,0),(8,0),(9,0),(11,0))]
            spritegroups[layername].add( Player(layername,tileid,x,y,imglist) )
        else:
            SpriteBuilder.basicSpriteFactory(spritegroups , layername,tileid,x,y,img)

#############################################################################

fps = 4 # frames per second
O = Ontology(True,'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
game = Game('Cartes/gardenofdelight.json',GardenSpriteBuilder)
game.mainiteration(60)

#############################################################################

def tournegauche():
    game.player.translate_sprite(0,0,-90)
    game.mainiteration(fps)


def tournedroite():
    game.player.translate_sprite(0,0,90)
    game.mainiteration(fps)

def avance():
    game.player.forward( game.player.rect.width )
    game.mainiteration(fps)
    return game.player.position_changed()

def ramasse():
    o = game.player.ramasse(game.groupDict)
    game.mainiteration(fps)
    return O.firstname(o)


def depose(nom=None):
    def _filtre(o): return nom in O.names(o)+[None]
    o = game.player.depose(game.groupDict , _filtre )
    game.mainiteration(fps)
    return O.firstname(o)

def cherche(nom=None):
    def _filtre(o): return nom in O.names(o)+[None]
    o = game.player.cherche_ramassable(game.groupDict,_filtre)
    game.mainiteration(fps)
    return O.firstname(o)

tg , td , av , ra , dp , ch = tournegauche , tournedroite , avance , ramasse , depose , cherche
