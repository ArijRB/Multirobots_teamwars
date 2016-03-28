import pygame
from math import pi,sqrt,cos,sin,floor
from core import polygons
import copy
import core.gameclass

class RecursiveDrawGroup(pygame.sprite.Group):
    """ Standard pygame.sprite.Group classes draw sprites by calling 'blit' on sprite images.
        Instead, this class calls 'draw' on each of its sprite """
    def draw(self,surf):
        for s in self:
            s.draw(surf)


class MySprite(pygame.sprite.Sprite):
    """ MySprite est un sprite qui connait l'image (ou les images) a afficher
    """

    def __init__(self,layername,tileid,x,y,imglist):
        pygame.sprite.Sprite.__init__(self)
        self.layername = layername
        self.tileid = tileid # tileid identifie le sprite sur la spritesheet. Generalement, c'est le row/col dans le spritesheet
        self.imagelist = imglist
        self.masklist  = [pygame.mask.from_surface(im) for im in imglist]
        self.set_new_image(imglist[0],x,y)

    def dist(self,x,y):
        cx,cy = self.get_centroid()
        return sqrt( (cx-x)**2 + (cy-y)**2 )

    def get_pos(self,backup=False):
        assert backup==False , "erreur: tentative d'acces a backup_rect d'un sprite non mobile"
        return (self.rect.x,self.rect.y)

    def draw(self,surf):
        surf.blit(self.image,self.rect)

    def set_new_image(self,img,x=None,y=None):
        self.image = img
        self.mask = pygame.mask.from_surface(img)
        if x is None or y is None:
            x,y = self.rect.x,self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x,y




class SurfaceViergeSprite(MySprite):
    def __init__(self,layername,x,y,w,h,couleur=(0,0,0)):
        img = pygame.Surface((w,h)).convert()
        img.set_colorkey( (0,0,0) )
        img.fill(couleur)
        MySprite.__init__(self,layername,tileid=None,x=x,y=y,imglist=[img])

class PointSprite(SurfaceViergeSprite):
    ''' just a point... can be useful ! '''
    def __init__(self,layername=None,x=0,y=0):
        SurfaceViergeSprite.__init__(self,layername,x=x,y=y,w=1,h=1,couleur=(255,255,255))




class DrawOnceSprite(pygame.sprite.Sprite):
    """ DrawOnceSprite est un sprite qui va s'afficher pendant quelques frames, puis s'autodetruire
        must be inside a RecursiveDrawGroup
    """
    lifespan = 1
    def __init__(self,drawfun,arglist):
        pygame.sprite.Sprite.__init__(self)
        self.drawfun = drawfun
        self.arglist = arglist
        self.lifespan = DrawOnceSprite.lifespan

    def draw(self,surf):
        self.drawfun(surf,*self.arglist)
        self.lifespan -= 1
        if self.lifespan == 0:
            self.kill()



class MovingSprite(MySprite):

    """ Cette classe represente les sprites qui peuvent bouger (ex: player, creatures, deplacable)
        les coordonnees ne sont plus stockees dans self.rect comme dans MySprite,
        mais dans self.x,self.y sous forme de flottant.
    """

    up_to_date = False # - is set to False each time a sprite changes (translation, rotation)
                       # - is set to True when the collision system has validated all changes
                       #   and when the backup and the current data coincide
                       #
                       #   Note: up_to_date is used only in synchronous mode

    def __init__(self,*args,**kwargs):

        MySprite.__init__(self,*args,**kwargs)

        self.x , self.y = self.rect.x , self.rect.y
        self.angle_degree  = 0
        self.auto_rotate_image = True

        self._backup()
        MovingSprite.up_to_date = False


    def _backup(self):
        self.backup_x , self.backup_y = self.x , self.y
        self.backup_angle_degree = self.angle_degree
        self.backup_image = self.image
        self.backup_mask  = self.mask
        self.resumed = False

    def _resume_to_backup(self):
        self.x , self.y = self.backup_x , self.backup_y
        self.rect.x , self.rect.y = int(self.x) , int(self.y)
        self.angle_degree = self.backup_angle_degree
        self.image = self.backup_image
        self.mask  = self.backup_mask
        self.resumed = True



    def get_pos(self,backup=False):
        return (int(self.backup_x),int(self.backup_y)) if backup else (int(self.x),int(self.y))

    def position_changed(self): return (self.backup_x,self.backup_y) != (self.x,self.y)

    def _rotate_image(self,a):
        """ this function computes new image based on angle a in degree
            because images are stored in imagelist, it simply selects the appropriate one
        """
        l = len(self.imagelist)
        i = int(floor( a*l/360 + 0.5 )) % l
        self.image = self.imagelist[ i ]
        self.mask =  self.masklist [ i ]


    def simple_translation(self,x,y,a,relative=True,check_collision_and_update=None):
        '''
        Attempts to translate and rotate a sprite.
        A collision test can be done with check_and_validate_collision.
        If test fails, then the translation+rotation backtracks

        :param x: unit in pixels
        :param y: unit in pixel
        :param a: angle in degree
        :param relative: boolean (if True then x,y,a parameters are relative to current position/orientation)
        :param check_collision_and_update:   This function checks if the new position/orientation yields a collision.
                                             If collision, then the function returns False
                                             If no collision, update collision data structure and return True

        :return: if collision test is done, it returns True of False depending on success or failure of test.
                 Otherwise returns None
        '''
        self._backup()
        if relative:
            self.x += x
            self.y += y
            self.angle_degree = (self.angle_degree + 720 + a) % 360
        else:
            self.x , self.y , self.angle_degree = x , y , a

        if self.auto_rotate_image:
            self._rotate_image(self.angle_degree)

        self.rect.x , self.rect.y = int(self.x) , int(self.y)
        #print('attempting to move sprite ',id(self),' to ',(self.rect.x , self.rect.y))


    def get_rowcol(self):
        assert int(self.x) % self.rect.w == 0 and int(self.y) % self.rect.h == 0, "sprite must not be accross tiles for this function"
        return int(self.y) // self.rect.h , int(self.x) // self.rect.w


    def get_centroid(self,entiers=False):   return self.position(entiers=False)
    def position(self,entiers=False):
        """
        position() renvoie un couple (x,y) representant les coordonnees du robot
                   ces coordonnees peuvent etre des flottants
        position(entiers=True) renvoie un couple de coordonnees entieres
        """
        cx,cy = self.x+self.rect.w//2,self.y+self.rect.h//2
        return (int(cx),int(cy)) if entiers else (cx,cy)

    def orientation(self):
        """
        orientation() renvoie l'angle en degres
        """
        return self.angle_degree




class Player(MovingSprite):
    '''
    A Player is an autonomous moving sprite
    It refreshed itself automatically,
    computes collisions and backtracks if necessary,
    displays itself automatically too
    '''

    def translate(self,x,y,a,relative=True):
        game = core.gameclass.get_game()
        MovingSprite.simple_translation(self,x,y,a,relative)

        r = game.mask.check_collision_and_update(self)
        if r:
            self._resume_to_backup()
            game.mask.check_collision_and_update(self)

        game.mainiteration(check_auto_refresh_flag=True)
        return not r


    def set_position(self,x,y):     return self.set_centroid(x,y)
    def set_centroid(self,x,y):
        """
        set_centroid(x,y) tente une teleportation du robot aux coordonnees x,y
        Renvoie False si la teleportation a echouee, pour cause d'obstacle
        """
        self.translate(x-self.rect.w//2,y-self.rect.h//2,self.angle_degree,relative=False)


    def rotate(self,deg):
        return self.translate(0,0, deg ,relative=True)

    def oriente(self,a):
        """
        oriente(a) fait pivoter le robot afin qu'il forme un angle de a degrees
        par rapport a l'horizontal.
        Donc oriente(0) le fait se tourner vers l'Est
        Donc oriente(90) le fait se tourner vers le Sud
        Donc oriente(-90) le fait se tourner vers le Nord
        Donc oriente(180) le fait se tourner vers l'Ouest
        """
        return self.translate(self.x,self.y,a,relative=False)

    def _forward_vector(self,t):
        dx,dy = cos(self.angle_degree * pi/180), sin(self.angle_degree * pi/180)
        if self.angle_degree % 90 == 0:
            dx,dy = round(dx),round(dy)
        return t*dx,t*dy


    def avance(self,t):     return self.forward(t)
    def forward(self,t):
        """
        p.forward()   deplace robot d'un pixel dans sa direction courante
        p.forward(x) le deplace de x pixels

        si dans x pixels il y a un obstacle, alors le deplacement echoue,
        et le robot reste a sa position courante et la fonction renvoie False.
        S'il n'y a pas d'obstacle la fonction renvoie True
        """
        vx,vy = self._forward_vector(t)
        return self.translate(vx,vy,0)


    def set_rowcol(self,row,col):
        return self.translate(col*self.rect.w,row*self.rect.h,self.angle_degree,relative=False)


    def tournegauche(self,a):
        """ tournegauche(a) pivote d'un angle donne, en degrees """
        return self.translate(0,0,-a,relative=True)


    def tournedroite(self,a):
        """ tournedroite(a) pivote d'un angle a donne, en degrees """
        return self.tournegauche(-a)

    def _obstacle_xy(self,x,y,relative):
        game = core.gameclass.get_game()
        MovingSprite.simple_translation(self,x,y,self.angle_degree,relative)
        r = game.mask.check_collision_and_update(self)
        self._resume_to_backup()
        game.mask.check_collision_and_update(self)
        return r

    def obstacle(self,s=1.0):
        """
        obstacle(x) verifie si un obstacle empeche le deplacement du robot de x pixel dans sa direction courante
        obstacle()  verifie la meme chose pour un deplacement de un pixel
        """
        x,y = self._forward_vector(s)
        return self._obstacle_xy(x,y,relative=True)


    def obstacle_coords(self,x,y):
        """
        obstacle_coords(x,y) verifie si aux coordonnees x,y il y a un
        obstacle qui empecherait le robot d'y etre
        renvoie True s'il y a un obstacle, False sinon
        """
        return self._obstacle_xy(x-self.rect.w//2,y-self.rect.h//2,relative=False)
