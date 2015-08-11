import pygame


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
