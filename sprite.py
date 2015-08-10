import pygame
from collisions import CollisionMask


class MySprite(pygame.sprite.Sprite):
    """ MySprite is a sprite which knows which image was used to build it
        tilerow/col are the coordinates of the sprite image in the spritesheet
    """
    tileid = (0,0) # tileid identifie le sprite sur la spritesheet. Generalement, c'est le row/col dans le spritesheet

    def __init__(self,layername,tileid,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.layername = layername
        self.tileid = tileid
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect  = self.image.get_rect()
        self.rect.x , self.rect.y = x,y



class MovingSprite(MySprite):

    """ This class represents the sprites that can move (ex: player, creatures, deplacable) """
    # vecteur vitesse requis. Si collision, alors il ne se realisera pas
    try_dx = 0
    try_dy = 0
    previous_rect = None

    def update(self,screen,collisionMask):
        """ Move the sprite. """
        MySprite.update(self)

        self.previous_rect = self.rect.copy()
        self.rect.x += self.try_dx
        self.rect.y += self.try_dy
        # ne pas sortir de l'ecran surtout !!!
        collisionMask.stay_inside_mask_area(self.rect)

        # si collision alors on ne bouge pas du tout
        if collisionMask.collide_sprite(self):
            self.rect = self.previous_rect

        self.stop()

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.try_dx = 0
        self.try_dy = 0



class Player(MovingSprite):

    def __init__(self,layername,tileid,x,y,img):
        MovingSprite.__init__(self,layername,tileid,x,y,img)
        self.inventory = pygame.sprite.Group()

    def move_with_keyboard(self,event,increment):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.try_dx = -increment
            if event.key == pygame.K_RIGHT:
                self.try_dx =  increment
            if event.key == pygame.K_UP:
                self.try_dy = -increment
            if event.key == pygame.K_DOWN:
                self.try_dy =  increment

    def ramasse_depose_with_keyboard(self,event,groupDict):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if self.cherche_ramassable(groupDict):
                    print "je suis sur un objet ramassable"
                else:
                    print "rien a ramasser"
            if event.key == pygame.K_r:
                o = self.ramasse(groupDict)
                if o == None:
                    print "rien a ramasser"
            if event.key == pygame.K_d:
                if self.depose(groupDict) == None:
                    print "rien a deposer"

    def cherche_ramassable(self,groupDict):
        for obj in groupDict["ramassable"]:
            if self.mask.overlap(obj.mask,(obj.rect.x - self.rect.x,obj.rect.y - self.rect.y)):
                return obj
        return None

    def ramasse(self,groupDict):
        o = self.cherche_ramassable(groupDict)
        if o == None:
            return None
        self.ramasse_objet(o,groupDict)
        return o

    def ramasse_objet(self,obj,groupDict):
        # remove object from existing groups displayed on the screen
        self.inventory.add( obj )
        obj.remove( groupDict.values() )

    def depose(self,groupDict):
        # remove object from existing groups displayed on the screen
        if not self.inventory:
            return None
        obj = list(self.inventory)[0]
        self.inventory.remove( obj )
        obj.rect.x , obj.rect.y = self.rect.x , self.rect.y
        groupDict[obj.layername].add( obj )
        return obj
