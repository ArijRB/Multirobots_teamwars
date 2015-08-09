import pygame


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


    def update(self,screen,obstaclegroup):
        """ Move the sprite. """

        # Move left/right
        self.rect.x += self.try_dx

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, obstaclegroup , False)

        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.try_dx > 0:
                self.rect.right = block.rect.left
            elif self.try_dx < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.try_dy

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, obstaclegroup, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.try_dy > 0:
                self.rect.bottom = block.rect.top
            elif self.try_dy < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            #self.try_dy = 0

        self.stop()

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.try_dx = 0
        self.try_dy = 0
        self.real_dx = 0
        self.real_dy = 0
