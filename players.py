import pygame
from sprite import MySprite,MovingSprite,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random
from math import pi,sqrt,cos,sin,floor
import rayon
import polygons
import glo
try:
    from pygame.gfxdraw import aacircle,filled_circle
    #filled_circle(surface, x, y, r, color) -> None
    #aacircle(surface, x, y, r, color) -> None
    def circle(surf,c,(x,y),r,w):
        filled_circle(surf,x,y,r,(20,20,60))
        aacircle(surf,x,y,r,c)
        aacircle(surf,x,y,r-1,c)

except:
    from pygame.draw import circle
    #circle(Surface, color, pos, radius, width=0) -> Rect

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

    def __init__(self,*args):
        Player.__init__(self,*args)
        cx,cy = self.get_centroid()
        w,h = self.rect.w , self.rect.h

        self.taille_geometrique = 22
        self.penwidth = 1
        self.typedessin = 'fleche' # is 'cercle' or 'fleche'
        self.tileid = None
        self.image = pygame.Surface((w,h)).convert()
        #pygame.gfxdraw.aacircle(self.image, w/2,h/2, self.taille_geometrique/2 - self.penwidth,glo.WHITE)
        circle(self.image, glo.WHITE, (w/2,h/2), self.taille_geometrique/2 - self.penwidth,self.penwidth)
        self.image.set_colorkey( (0,0,0) )
        self.imagelist = [self.image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.w,self.rect.h = self.image.get_rect().w,self.image.get_rect().h

    def build_dessin(self):
        w,h = self.rect.w , self.rect.h
        self.dessin = pygame.Surface((w,h)).convert()
        self.dessin.set_colorkey( (0,0,0) )
        #self.dessin.set_alpha(250)
        self.draw_dessin()

    def draw(self,surf):
        cx,cy = self.get_centroid()
        Player.draw(self,surf)
        if self.dessin:
            surf.blit(self.dessin,self.rect)

    def draw_dessin(self):
        self.backup_angle_degree = self.angle_degree
        self.dessin.fill((0,0,0))
        w,h = self.rect.w , self.rect.h
        if self.typedessin == 'fleche':
            polygons.draw_arrow(self.dessin,w/2,h/2,self.angle_degree * pi/180,r=self.taille_geometrique-14,clr=glo.WHITE)
        elif self.typedessin == 'cercle':
            x1,y1,x2,y2 = w/2,h/2,int(w/2+(self.taille_geometrique/2-1)*cos(self.angle_degree * pi/180)),int(h/2+(self.taille_geometrique/2-1)*sin(self.angle_degree * pi/180))
            pygame.draw.line(self.dessin,glo.WHITE,(x1,y1),(x2,y2),2)
            #pygame.gfxdraw.line(self.dessin,x1,y1,x2,y2,glo.WHITE)
            #polygons.draw_arrow(self.dessin,w/2,h/2,self.angle_degree * pi/180,r=self.taille_geometrique-14,clr=glo.WHITE)
        else:
            raise 'erreur: le dessin de la tortue peut etre un cercle ou une fleche'


    def update(self):
        super(Turtle, self).update()

        if self.dessin:
            if self.backup_angle_degree != self.angle_degree:
                self.draw_dessin()
