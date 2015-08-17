import pygame
from collisions import CollisionMask
import random
import math
import rayon

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

    def get_pos(self,backup=False):
        assert backup==False , "erreur: tentative d'acces a backup_rect d'un sprite non mobile"
        return (self.rect.x,self.rect.y)



class MovingSprite(MySprite):

    """ This class represents the sprites that can move (ex: player, creatures, deplacable) """
    # vecteur vitesse requis. Si collision, alors il ne se realisera pas

    def __init__(self,*args):
        MySprite.__init__(self,*args)
        self.backup_rect = self.rect.copy()

    def backup_position(self):
        self.backup_rect.x , self.backup_rect.y = self.rect.x , self.rect.y

    def resume_position_to_backup(self):
        self.rect.x , self.rect.y = self.backup_rect.x , self.backup_rect.y

    def get_pos(self,backup=False):
        return (self.backup_rect.x,self.backup_rect.y) if backup else (self.rect.x,self.rect.y)

    def position_changed(self): return self.backup_rect != self.rect

    def translate_sprite(self,x,y,relative=True,boundingrect=None):
        # Attention, backup_position() est indispensable,
        # car la gestion des collision doit pouvoir revenir en arriere
        self.backup_position()

        if relative:
            self.rect.move_ip(x,y)
        else:
            self.rect.x , self.rect.y = x , y

        if boundingrect:
            w , h = boundingrect.get_size()
            w -= self.rect.w
            h -= self.rect.h
            if self.rect.x >= w:     self.rect.x = w
            if self.rect.x < 0:      self.rect.x = 0
            if self.rect.y >= h:     self.rect.y = h
            if self.rect.y < 0:      self.rect.y = 0






class Player(MovingSprite):

    def __init__(self,*args):
        MovingSprite.__init__(self,*args)
        self.inventory = pygame.sprite.Group()

    def move_with_keyboard(self,event,increment):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.translate_sprite(-increment,0)
            if event.key == pygame.K_RIGHT:
                self.translate_sprite(increment,0)
            if event.key == pygame.K_UP:
                self.translate_sprite(0,-increment)
            if event.key == pygame.K_DOWN:
                self.translate_sprite(0,increment)

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

    def throw_ray_with_keyboard(self,event,mask):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                mask.erase_sprite( self )
                angle = random.random()*2*math.pi
                w,h = mask.mask.get_size()
                self.center_x , self.center_y = self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2
                rayon_hit = rayon.rayon(mask.mask,self.center_x , self.center_y,angle,w,h)
                mask.draw_sprite( self )
                return rayon_hit
