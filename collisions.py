import pygame


class CollisionMask:

    def __init__(self,screen):
        self.mask = pygame.mask.from_surface(screen)
        self.mask.clear()
        #self.mask = build_collision_mask(self.obstacleMask,self.screen,self.groupDict):

    def add_sprite(self,spr):
        self.mask.draw(spr.mask,(spr.rect.x,spr.rect.y) )

    def fill_with_group(self,group):
            self.mask.clear()
            for spr in group:
                self.mask.draw(spr.mask,(spr.rect.x,spr.rect.y) )

    def collide_sprite(self,spr):
        return self.mask.overlap(spr.mask,(spr.rect.x,spr.rect.y))
