from spritebuilder import SpriteBuilder
import constants
import pygame
from collections import OrderedDict
import random
try:
    from toolz import first
except:
    first = lambda x: list(x)[0]


from collisions import CollisionMask


class Game:

    # callbacks is a dictionary of functions to call depending on key pressed
    callbacks = {}

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


    def setup_keyboard_callbacks(self):
        self.callbacks = self.player.gen_callbacks(self.player.rect.w,self.groupDict,self.mask)


    def update(self):
        self.mask.compute_collision(self.groupDict,self.player)

        for layer in constants.NON_BG_LAYERS:
            self.groupDict[layer].update()

    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        for layer in constants.NON_BG_LAYERS:
            self.groupDict[layer].draw(self.screen)

        pygame.display.flip()


    def mainiteration(self):
        if pygame.event.peek():
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in self.callbacks:
                        self.callbacks[event.key]()

        self.update()
        self.draw()
        self.clock.tick(60)

    def mainloop(self):
        while True:
            self.mainiteration()
