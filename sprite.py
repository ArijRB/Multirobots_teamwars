import pygame
from collisions import CollisionMask


class MySprite(pygame.sprite.Sprite):
    """ MySprite is a sprite which knows which image was used to build it
        tilerow/col are the coordinates of the sprite image in the spritesheet
    """
    tileid = (0,0) # tileid identifie le sprite sur la spritesheet. Generalement, c'est le row/col dans le spritesheet

    def __init__(self,tileid,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.tileid = tileid
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect  = self.image.get_rect()
        self.rect.x , self.rect.y = x,y



class MovingSprite(MySprite):
    """ This class represents the sprites that can move (ex: player, creatures, deplacable) """

    # -- Attributes
    # vecteur vitesse requis. Si collision, alors il ne se realisera pas
    try_dx = 0
    try_dy = 0

    # vecteur vitesse reel, obtenu apres collision
    real_dx = 0
    real_dy = 0


    def update(self,screen,collisionMask):
        """ Move the sprite. """

        initrect = self.rect.copy()
        self.rect.x += self.try_dx
        self.rect.y += self.try_dy

        # si collision alors on ne bouge pas du tout
        if collisionMask.collide_sprite(self):
            self.rect = initrect
            self.real_dx,self.real_dy = 0,0
        else:
            self.real_dx,self.real_dy = self.try_dx,self.try_dy

        # ne pas sortir de l'ecran surtout !!!
        w , h = collisionMask.mask.get_size()
        if self.rect.x >= w:     self.rect.x = w
        if self.rect.x < 0:      self.rect.x = 0
        if self.rect.y >= h:     self.rect.y = h
        if self.rect.y < 0:      self.rect.y = 0

        self.stop()

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.try_dx = 0
        self.try_dy = 0
