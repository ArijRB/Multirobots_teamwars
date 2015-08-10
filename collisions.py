import pygame


class CollisionMask:

    def __init__(self,screen):
        self.mask = pygame.mask.from_surface(screen)
        self.mask.clear()

    def add_sprite(self,spr):
        self.mask.draw(spr.mask,(spr.rect.x,spr.rect.y) )

    def fill_with_group(self,group):
            self.mask.clear()
            for spr in group:
                self.mask.draw(spr.mask,(spr.rect.x,spr.rect.y) )

    def collide_sprite(self,spr):
        return self.mask.overlap(spr.mask,(spr.rect.x,spr.rect.y))

    def stay_inside_mask_area(self,r):
        w , h = self.mask.get_size()
        w -= r.w
        h -= r.h
        if r.x >= w:     r.x = w
        if r.x < 0:      r.x = 0
        if r.y >= h:     r.y = h
        if r.y < 0:      r.y = 0
