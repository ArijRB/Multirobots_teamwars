import pygame
from sprite import MySprite,MovingSprite,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random
from itertools import izip
from math import pi,sqrt,cos,sin,floor
import rayon
import polygons
import glo
try:
    from pygame.gfxdraw import aacircle,filled_circle
    def circle(surf,c,(x,y),r,w):
        filled_circle(surf,x,y,r,(20,20,60))
        aacircle(surf,x,y,r,c)
        aacircle(surf,x,y,r-1,c)
except:
    from pygame.draw import circle


class Player(MovingSprite):
    """ cette classe modelise un sprite controlable par l'utilisateur
        soit au tile pres, soit au pixel pres
        soit au clavier directement, soit par instructions
    """
    def __init__(self,*args,**kwargs):
        MovingSprite.__init__(self,*args,**kwargs)
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

    def throw_ray(self,radian_angle,mask,groupDict,coords=None):
        mask.erase_sprite( self )
        cx,cy = coords if coords else self.get_centroid()
        w,h = mask.mask.get_size()
        if radian_angle is None: radian_angle = random()*2*pi
        self.rayon_hit = rayon.rayon(mask.mask,cx,cy,radian_angle,w,h)
        mask.draw_sprite( self )
        if self.rayon_hit and groupDict:
            groupDict["eye_candy"].add( DrawOnceSprite( pygame.draw.line , [(255,0,0),(cx,cy),self.rayon_hit,4] ) )
        return self.rayon_hit


class Turtle(Player):
    def __init__(self,layername,x,y,w,h):
        self.taille_geometrique, self.penwidth = 22, 1
        Player.__init__(self,layername,tileid=None,x=x,y=y,imglist=self.build_Turtle_list_images(w,h))

    def build_Turtle_list_images(self,w,h):
        """ cree 360 images de tortues (une par degre)"""
        imglist = [pygame.Surface((w,h)).convert() for a in range(360)]
        for a,img in izip(range(360),imglist):
            img.set_colorkey( (0,0,0) )
            img.fill((0,0,0))
            circle(img, glo.WHITE, (w/2,h/2), self.taille_geometrique/2 - self.penwidth,self.penwidth)
            polygons.draw_arrow(img,w/2,h/2,a * pi/180,r=self.taille_geometrique-14,clr=glo.WHITE)
            #pygame.gfxdraw.aacircle(self.image, w/2,h/2, self.taille_geometrique/2 - self.penwidth,glo.WHITE)
        return imglist
