from gameclass import Game
from spritebuilder import SpriteBuilder
from players import Player
from ontology import Ontology
import pygame
import glo


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

class gw:
    game = None
    fps  = None
    O    = None
    name = 'gardenofdelight'

def init(_boardname = None):
    pygame.quit()
    if _boardname: gw.name = _boardname
    gw.fps = 4 # frames per second
    gw.O   = Ontology(True,'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    gw.game= Game('Cartes/' + gw.name + '.json',GardenSpriteBuilder)
    gw.game.mainiteration(60)



def tournegauche():
    gw.game.player.translate_sprite(0,0,-90)
    gw.game.mainiteration(gw.fps)


def tournedroite():
    gw.game.player.translate_sprite(0,0,90)
    gw.game.mainiteration(gw.fps)

def avance():
    gw.game.player.forward( gw.game.player.rect.width )
    gw.game.mainiteration(gw.fps)
    return gw.game.player.position_changed()

def ramasse():
    o = gw.game.player.ramasse(gw.game.groupDict)
    gw.game.mainiteration(gw.fps)
    return gw.O.firstname(o)


def depose(nom=None):
    def _filtre(o): return nom in gw.O.names(o)+[None]
    o = gw.game.player.depose(gw.game.groupDict , _filtre )
    gw.game.mainiteration(gw.fps)
    return gw.O.firstname(o)

def cherche(nom=None):
    def _filtre(o): return nom in gw.O.names(o)+[None]
    o = gw.game.player.cherche_ramassable(gw.game.groupDict,_filtre)
    gw.game.mainiteration(gw.fps)
    return gw.O.firstname(o)

tg , td , av , ra , dp , ch , reset = tournegauche , tournedroite , avance , ramasse , depose , cherche , init
