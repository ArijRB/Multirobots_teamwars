from spritebuilder import SpriteBuilder
import constants
import pygame
from collections import OrderedDict
try:
    from toolz import first
except:
    first = lambda x: list(x)[0]

from collisions import CollisionMask

class Game:

    def __init__(self,fichiercarte,_SpriteBuilder):

        pygame.init()

        # charge la carte et le spritesheet
        self.spriteBuilder = _SpriteBuilder(fichiercarte)

        # cree la fenetre pygame
        self.screen = pygame.display.set_mode([ self.spriteBuilder.spritesize*self.spriteBuilder.rowsize ,
                                                self.spriteBuilder.spritesize*self.spriteBuilder.colsize ])
        pygame.display.set_caption("pySpriteWorld Experiment")

        # converti les sprites meme format que l'ecran
        self.spriteBuilder.prepareSprites()

        # cree un groupe de sprites pour chaque layer
        self.groupDict = self.spriteBuilder.buildGroups()
        # cherche le premier sprite joueur
        try:
            self.player = first(self.groupDict["joueur"])
        except Exception:
            raise IndexError("Je ne trouve aucun joueur dans le fichier TMX")

        # prepare le bitmap 'background'
        self.background = pygame.Surface([ self.screen.get_width(), self.screen.get_height() ]).convert()
        self.groupDict["bg1"].draw(self.background)
        self.groupDict["bg2"].draw(self.background)

        # cree un masque de la taille de l'ecran, pour le calcul des collisions
        self.mask = CollisionMask(self.screen)

        # click clock
        self.clock = pygame.time.Clock()


    def update(self):
        # computes collisions mask of all obstacles (for pixel-based collisions)
        self.mask.fill_with_group( self.groupDict["obstacles"] )

        # send it to the players
        self.groupDict["joueur"].update(self.screen,self.mask)


    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))

        for layer in constants.NON_BG_LAYERS:
            self.groupDict[layer].draw(self.screen)

        self.clock.tick(60)
        pygame.display.flip()
