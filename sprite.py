import pygame
from collisions import CollisionMask
from random import random
from math import pi,sqrt,cos,sin
import rayon
import polygons
from functools import partial

class RecursiveDrawGroup(pygame.sprite.Group):
    """ Standard pygame.sprite.Group classes draw sprites by calling 'blit' on sprite images.
        Instead, this class calls 'draw' on each of its sprite """
    def draw(self,surf):
        for s in self:
            s.draw(surf)


class MySprite(pygame.sprite.Sprite):
    """ MySprite est un sprite qui connait l'image a afficher
    """
    tileid = (0,0) # tileid identifie le sprite sur la spritesheet. Generalement, c'est le row/col dans le spritesheet

    def __init__(self,layername,tileid,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.layername = layername
        self.tileid = tileid
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = img.get_rect()
        self.rect.x , self.rect.y = x,y

    def dist(self,x,y):
        cx,cy = self.get_centroid()
        return sqrt( (cx-x)**2 + (cy-y)**2 )

    def get_pos(self,backup=False):
        assert backup==False , "erreur: tentative d'acces a backup_rect d'un sprite non mobile"
        return (self.rect.x,self.rect.y)

    def draw(self,surf):
        surf.blit(self.image,self.rect)

class DrawOnceSprite(pygame.sprite.Sprite):
    def __init__(self,fun,arglist):
        pygame.sprite.Sprite.__init__(self)
        self.fun = fun
        self.arglist = arglist
        self.lifespan = 5
    def draw(self,surf):
        self.fun(surf,*self.arglist)
        self.lifespan -= 1
        if self.lifespan == 0:
            self.kill()



class MovingSprite(MySprite):

    """ Cette classe represente les sprites qui peuvent bouger (ex: player, creatures, deplacable)
        les coordonnees ne sont plus stockees dans self.rect comme dans MySprite,
        mais dans self.x,self.y sous forme de flottant.
    """

    # vecteur vitesse requis. Si collision, alors il ne se realisera pas

    def __init__(self,*args):
        MySprite.__init__(self,*args)
        self.x , self.y = self.rect.x , self.rect.y
        self.backup_position()

    def backup_position(self):
        self.backup_x , self.backup_y = self.x , self.y

    def resume_position_to_backup(self):
        self.x , self.y = self.backup_x , self.backup_y

    def get_pos(self,backup=False):
        return (int(self.backup_x),int(self.backup_y)) if backup else (int(self.x),int(self.y))

    def position_changed(self): return (self.backup_x,self.backup_y) != (self.x,self.y)

    def translate_sprite(self,x,y,relative=True,boundingrect=None):
        # Attention, backup_position() est indispensable,
        # car la gestion des collision doit pouvoir revenir en arriere
        self.backup_position()

        if relative:
            self.x += x
            self.y += y
        else:
            self.x , self.y = x , y

        if boundingrect:
            w , h = boundingrect.get_size()
            w -= self.rect.w
            h -= self.rect.h
            if self.x >= w:     self.x = w
            if self.x < 0:      self.x = 0
            if self.y >= h:     self.y = h
            if self.y < 0:      self.y = 0

    def set_centroid(self,x,y):
        self.translate_sprite(x-self.rect.w,y-self.rect.h,relative=False)

    def get_centroid(self):
        return self.x+self.rect.w/2,self.y+self.rect.h/2

    def update(self):
        self.rect.x , self.rect.y = int(self.x) , int(self.y)



class Player(MovingSprite):

    def __init__(self,*args):
        MovingSprite.__init__(self,*args)
        self.inventory = pygame.sprite.Group()

    def gen_callbacks(self,incr,gDict,mask):
        transl = self.translate_sprite
        return {
            pygame.K_LEFT:  partial(transl,x= -incr , y=0),
            pygame.K_RIGHT: partial(transl,x=  incr , y=0),
            pygame.K_UP:    partial(transl,x=  0    , y= -incr),
            pygame.K_DOWN:  partial(transl,x=  0    , y=  incr),
            pygame.K_c:     partial(self.cherche_ramassable,groupDict=gDict,verb=True),
            pygame.K_r:     partial(self.ramasse,groupDict=gDict,verb=True),
            pygame.K_d:     partial(self.depose,groupDict=gDict,verb=True),
            pygame.K_t:     partial(self.throw_ray,radian_angle=None,mask=mask,groupDict=gDict)
        }


    def cherche_ramassable(self,groupDict,verb=False):
        for obj in groupDict["ramassable"]:
            if self.mask.overlap(obj.mask,(obj.x - self.x,obj.y - self.y)):
                if verb: print "je suis sur un objet ramassable"
                return obj
        if verb: print "rien a ramasser"
        return None

    def ramasse(self,groupDict,verb=False):
        o = self.cherche_ramassable(groupDict)
        if o == None:
            if verb: print "rien a ramasser"
            return None
        self.ramasse_objet(o,groupDict)
        return o

    def ramasse_objet(self,obj,groupDict):
        # remove object from existing groups displayed on the screen
        self.inventory.add( obj )
        obj.remove( groupDict.values() )

    def depose(self,groupDict,verb=False):
        # remove object from existing groups displayed on the screen
        if not self.inventory:
            if verb: print "rien a deposer"
            return None
        obj = list(self.inventory)[0]
        self.inventory.remove( obj )
        obj.translate_sprite(self.x,self.y,False)
        groupDict[obj.layername].add( obj )
        return obj

    def throw_ray(self,radian_angle,mask,groupDict):
        mask.erase_sprite( self )
        cx,cy = self.get_centroid()
        w,h = mask.mask.get_size()
        if radian_angle==None: radian_angle = random()*2*pi
        self.rayon_hit = rayon.rayon(mask.mask,cx,cy,radian_angle,w,h)
        mask.draw_sprite( self )
        if self.rayon_hit and groupDict:
            groupDict["eye_candy"].add( DrawOnceSprite( pygame.draw.line , [(255,0,0),self.get_centroid(),self.rayon_hit,4] ) )
        return self.rayon_hit



class Turtle(Player):

    angle_degree  = 90
    backup_angle_degree = None

    taille_fleche = 40
    fleche = None

    def build_fleche(self):
        self.fleche = pygame.Surface((self.taille_fleche,self.taille_fleche))
        self.fleche.set_colorkey( (0,0,0) )
        self.fleche.set_alpha(150)

    def draw(self,surf):
        cx,cy = self.get_centroid()
        if self.fleche:
            surf.blit(self.fleche,(cx-self.taille_fleche/2,cy-self.taille_fleche/2))

        Player.draw(self,surf)

    def update(self):
        super(Turtle, self).update()

        if self.fleche:
            if self.backup_angle_degree != self.angle_degree:
                self.backup_angle_degree = self.angle_degree
                self.fleche.fill((0,0,0))
                polygons.draw_arrow(self.fleche,self.taille_fleche/2,self.taille_fleche/2,self.angle_degree * pi/180)

    def forward(self,t):
        self.translate_sprite(t*cos(self.angle_degree * pi/180),t*sin(self.angle_degree * pi/180))

    def rotate(self,a,relative=True):
        self.angle_degree = (self.angle_degree + 720 + a) % 360 if relative else a
