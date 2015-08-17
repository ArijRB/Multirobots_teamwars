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


    def collisions_single_player(self):
        # computes collisions mask of all obstacles (for pixel-based collisions)
        self.mask.fill_with_group( self.groupDict["obstacles"] )

        # send it to the player
        assert not self.mask.collide_sprite( self.player , True ) , "sprite collision before any movement !!!"
        if self.mask.collide_sprite( self.player ):
            self.player.resume_position_to_backup()


    def collisions_many_players(self):
        joueurs = list(self.groupDict["joueur"])
        random.shuffle( joueurs )

        self.mask.fill_with_group( self.groupDict["obstacles"] )

        # test if sprites at backup position do not collide anything and draw them on the mask
        for j in joueurs:
            assert not self.mask.collide_sprite( j , True ) , "sprite collision before any movement !!!"
            self.mask.draw_sprite(j,backup=True)

        # try their new position one by one
        for j in joueurs:
            self.mask.erase_sprite( j , backup = True )
            if self.mask.collide_sprite( j ):
                j.resume_position_to_backup()
            self.mask.draw_sprite(j)


    def update(self,event):
        if len(self.groupDict["joueur"]) == 1:
            self.collisions_single_player()
        else:
            self.collisions_many_players()


    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))

        for layer in constants.NON_BG_LAYERS:
            self.groupDict[layer].draw(self.screen)

        self.clock.tick(60)
        pygame.display.flip()

    def mainloop(self):
        while True:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    pygame.quit()
                    quit()

                self.update(event)
            self.draw()
