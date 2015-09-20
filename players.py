import pygame
from sprite import MySprite,MovingSprite,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random
from math import pi,sqrt,cos,sin,floor
import rayon
import polygons


class Player(MovingSprite):
    """ cette classe modelise un sprite controlable par l'utilisateur
        soit au tile pres, soit au pixel pres
        soit au clavier directement, soit par instructions
    """
    def __init__(self,*args):
        MovingSprite.__init__(self,*args)
        self.inventory = pygame.sprite.Group()

    def gen_callbacks(self,incr,gDict,mask):
        transl = self.translate_sprite
        return {
            pygame.K_LEFT:  partial(transl,x= -incr , y=0, a=0),
            pygame.K_RIGHT: partial(transl,x=  incr , y=0, a=0),
            pygame.K_UP:    partial(transl,x=  0    , y= -incr, a=0),
            pygame.K_DOWN:  partial(transl,x=  0    , y=  incr, a=0),
            pygame.K_c:     partial(self.cherche_ramassable,groupDict=gDict,verb=True),
            pygame.K_r:     partial(self.ramasse,groupDict=gDict,verb=True),
            pygame.K_d:     partial(self.depose,groupDict=gDict,verb=True),
            pygame.K_t:     partial(self.throw_ray,radian_angle=None,mask=mask,groupDict=gDict)
        }


    def cherche_ramassable(self,groupDict,filtre = lambda x:True,verb=False):
        for obj in groupDict["ramassable"]:
            if filtre(obj):
                if self.mask.overlap(obj.mask,(obj.rect.x - self.rect.x,obj.rect.y - self.rect.y)):
                    if verb: print ("j'en ai trouve un")
                    return obj
        if verb: print ("rien a ramasser")
        return None

    def ramasse(self,groupDict,verb=False):
        o = self.cherche_ramassable(groupDict)
        if o is None:
            if verb: print ("rien a ramasser")
            return None
        self.inventory.add( o )
        o.remove( groupDict.values() )
        return o


    def depose(self,groupDict,filtre = lambda x:True,verb=False):
        # remove object from existing groups displayed on the screen
        candidats = [o for o in self.inventory if filtre(o)]

        if not candidats:
            if verb: print ("rien a deposer")
            return None
        obj = candidats[0]
        self.inventory.remove( obj )
        obj.translate_sprite(self.x,self.y,0,False)
        groupDict[obj.layername].add( obj )
        return obj

    def throw_ray(self,radian_angle,mask,groupDict):
        mask.erase_sprite( self )
        cx,cy = self.get_centroid()
        w,h = mask.mask.get_size()
        if radian_angle is None: radian_angle = random()*2*pi
        self.rayon_hit = rayon.rayon(mask.mask,cx,cy,radian_angle,w,h)
        mask.draw_sprite( self )
        if self.rayon_hit and groupDict:
            groupDict["eye_candy"].add( DrawOnceSprite( pygame.draw.line , [(255,0,0),self.get_centroid(),self.rayon_hit,4] ) )
        return self.rayon_hit



class Turtle(Player):

    def __init__(self,*args):
        Player.__init__(self,*args)
        self.taille_fleche = 40
        self.fleche = None

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
