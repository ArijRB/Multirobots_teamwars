import pygame
import random

class CollisionMask:

    def __init__(self,screen):
        self.mask = pygame.mask.from_surface(screen)
        self.mask.clear()

    def draw_sprite(self,spr,backup=False):
        self.mask.draw(spr.mask, spr.get_pos(backup) )


    def erase_sprite(self,spr,backup=False):
        self.mask.erase(spr.mask,spr.get_pos(backup) )

    def collide_sprite(self,spr,backup=False):
        return self.mask.overlap(spr.mask, spr.get_pos(backup) )


    def fill_with_group(self,group,backup=False):
            self.mask.clear()
            for spr in group:
                self.mask.draw(spr.mask, spr.get_pos(backup) )

    ###############  compute collision ###################

    def compute_collision(self,gDict,player):
        if len(gDict["joueur"]) > 1:
            self.collisions_many_players(gDict)
        else:
            self.collisions_single_player(gDict,player)


    def collisions_single_player(self,gDict,player):
        # computes collisions mask of all obstacles (for pixel-based collisions)
        self.fill_with_group( gDict["obstacles"] )

        # send it to the player
        assert not self.collide_sprite( player , True ) , "sprite collision before any movement !!!"
        if self.collide_sprite( player ):
            player.resume_position_to_backup()


    def collisions_many_players(self,gDict):
        joueurs = list(gDict["joueur"])
        random.shuffle( joueurs )

        self.fill_with_group( gDict["obstacles"] )

        # test if sprites at backup position do not collide anything and draw them on the mask
        for j in joueurs:
            assert not self.collide_sprite( j , True ) , "sprite collision before any movement !!!"
            self.draw_sprite(j,backup=True)

        # try their new position one by one
        for j in joueurs:
            self.erase_sprite( j , backup = True )
            if self.collide_sprite( j ):
                j.resume_position_to_backup()
            self.draw_sprite(j)
