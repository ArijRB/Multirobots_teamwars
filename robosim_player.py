import pygame
from core.sprite import MySprite,MovingSprite,Player,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random
from math import pi,sqrt,cos,sin,floor
from core import rayon
from core import polygons
from core import glo
from collections import namedtuple
import core.gameclass


try:
    from pygame.gfxdraw import aacircle,filled_circle
    def circle(surf,c,coord,r,w):
        x,y = coord
        x,y,r = int(x),int(y),int(r)
        filled_circle(surf,x,y,r,(20,20,60))
        aacircle(surf,x,y,r,c)
        aacircle(surf,x,y,r-1,c)
except:
    from pygame.draw import circle




class Turtle(Player):
    static_imglist = None
    w,h = None,None
    diametre, penwidth = 22, 1

    @classmethod
    def set_turtle_size(cls,diametre):
        Turtle.diametre = diametre

    @classmethod
    def build_Turtle_list_images(cls):
        """ cree 360 images de tortues (une par degre)"""
        w = Turtle.diametre + Turtle.penwidth*2
        Turtle.static_imglist = [pygame.Surface((w,w)).convert() for a in range(360)]
        for a,img in zip(range(360),Turtle.static_imglist):
            img.set_colorkey( (0,0,0) )
            img.fill((0,0,0))
            circle(img, glo.WHITE, (w/2,w/2), Turtle.diametre/2 - Turtle.penwidth,Turtle.penwidth)
            polygons.draw_arrow(img,w/2,w/2,a * pi/180,r=Turtle.diametre-14,clr=glo.WHITE)
            #pygame.gfxdraw.aacircle(self.image, w/2,h/2, self.taille_geometrique/2 - self.penwidth,glo.WHITE)
        return Turtle.static_imglist

    def diametre_robot(self):
        return self.diametre

    def __init__(self,layername,x,y):
        if Turtle.static_imglist is None:
            Turtle.build_Turtle_list_images()
        Player.__init__(self,layername,tileid=None,x=x,y=y,imglist=Turtle.build_Turtle_list_images())


    def telemetre(self,from_center=False,rel_angle=0):
        """
        telemetre(from_center=False,rel_angle=0)

        telemetre() tire un rayon laser dans la direction du robot
        la fonction renvoie le nombre de pixels que le robot peut parcourir avant
        de rencontrer un obstacle.
        telemetre(from_center=True) compte le nombre de pixels depuis le centre du robot (et non pas le bord)
        telemetre(rel_angle) tire le rayon avec l'angle rel_angle (relativement a l'orientation du robot)
        """
        game = core.gameclass.get_game()
        game.mask.update_bitmasks(game.layers)
        rayon_hit = unsafe_throw_rays(self,[rel_angle],game,coords=None,relative=True,show_rays=True)[0]

        game.mainiteration(check_auto_refresh_flag=True)

        d = self.dist(*rayon_hit)
        return d if from_center else d-(self.diametre_robot()//2)


    def pendown(self):
        """
        pendown() abaisse le stylo
        """
        self.usepen = True


    def penup(self):
        """
        penup() releve le stylo
        """
        self.usepen = False



###### Functions outside the Turtle class #######

def unsafe_throw_rays(player,angle_degree_list,game,coords=None,relative=False,max_radius=None,show_rays=False):
    """
    This function is 'unsafe' because before calling it, the mask MUST be up-to-date
    To update it, call game.mask.update_bitmasks(game.layers)
    either coords or player needs to be not None

    >>> x,y = unsafe_throw_rays(game.player,[-90,90],game,relative=True,show_rays=True)
    # This will shoot two rays from the center of the player, one on each side of the player.
    # rays will be displayed
    >>> x,y = unsafe_throw_rays(player=None,[-90,0,90,180],game,coords=(256,256),relative=False,show_rays=False)
    # This will shoot four rays in the four directions (south,east,north,west) from the center of the screen
    """

    assert not (relative and player is None) and not (player is None and coords is None)
    m   = game.mask

    w,h = m.mask_players.get_size()
    cx,cy = coords if coords else player.get_centroid()
    if player is not None: m._erase_player_mask( player )

    rel = player.angle_degree if relative else 0.0

    r = [rayon.rayon(m.mask_players,m.mask_obstacles,cx,cy,rel+a,w,h,max_radius) for a in angle_degree_list]

    if player is not None: m._draw_player_mask( player )
    if show_rays:
        for h in r:
            game.layers["dessinable"].add( DrawOnceSprite( pygame.draw.line , [(255,0,0),(cx,cy),h,4] ) )
    return r


RayImpactTuple = namedtuple('RayImpactTuple', ['sprite','layer','x', 'y','dist_from_border','dist_from_center','rel_angle_degree','abs_angle_degree'])

def build_RayImpact_info(player,game,hitlist,angle_degree_list=None):
    '''
    build_RayImpact_info takes a hitlist (output of unsafe_throw_rays for example)
    and outputs a list of RayImpactTuple, giving collision information.
    '''
    ray_info = []
    for i,(x,y) in enumerate(hitlist):
        dis = player.dist( x,y )
        try:    d_border = dis - player.diametre//2
        except: d_border = None

        l = game.mask.who_is_at(x,y,{'obstacle','joueur'})
        s2,lay = (l[0],l[0].layername) if l else (None,None)

        angle = None if angle_degree_list is None else angle_degree_list[i]

        ray_info.append( RayImpactTuple(sprite=s2,layer=lay,x=x,y=y,dist_from_border=d_border,dist_from_center=dis,
                                        rel_angle_degree=angle,
                                        abs_angle_degree=angle+player.orientation() ) )

    return ray_info


def telemetre_coords_list(x,y,angle_degree_list,show_rays=True,p=None):
    """
    telemetre_coords_list(x,y,angle_degree_list,show_rays=True)
    tire un rayon laser depuis x,y avec les angles angle_list
    la fonction renvoie une liste contenant les nombres de pixels parcourus par le rayon avant
    de rencontrer un obstacle
    """
    game = core.gameclass.get_game()
    game.mask.update_bitmasks(game.layers)
    p = game.player if p is None else p
    x,y = int(x),int(y)

    hitlist = unsafe_throw_rays(p,angle_degree_list , game,coords=(x,y),show_rays=show_rays)
    game.mainiteration(check_auto_refresh_flag=True)
    return [sqrt( (rx-x)**2 + (ry-y)**2 ) for rx,ry in hitlist]


def telemetre_coords(x,y,a):
    """ voir telemetre_coords_list """
    return telemetre_coords_list(x,y,[a])[0]




def throw_rays_for_many_players(game,player_collection,angle_degree_list,max_radius=None,show_rays=False):
    '''
    For each player, throws rays along specified angles,
    and returns collisions as a dictionary

    Example of use:
    Let us call this function on a single player.
    Assume the first ray hits an obstacle sprite s1 at (120,33),
    the second ray hits the limits of window at (512,395) and
    the third ray hits a player sprite s2 in (153,57)

    >>> d = throw_rays_for_many_players(game, [game.player] , [-45, 0, 45] )
    >>> d[ game.player ]
    [ (s1,'obstacle',120,33,83.2,90.3), (None,None,512,395,140,149), (s2,'joueur',153,57,53.8,62.1) ]
    >>> d[ game.player ][0].x , d[ game.player ][0].y
    (120,33)
    >>> d[ game.player ][0].layer == 'obstacle'
    True
    >>> d[ game.player ][1].dist_from_center
    62.1

    :param player_collection: list or group of players which have to throw rays
    :param radian_angle_list: list of angles (in radian), relative to players
    :param show_rays: boolean, display or not display red lines.
    :return: dictionary d of players:RayImpactTuple, for each player in player_collection.

    '''
    game.mask.update_bitmasks(game.layers)
    d = {}

    for p in player_collection:
        hitlist = unsafe_throw_rays(p,angle_degree_list,game,relative=True,max_radius=max_radius,show_rays=show_rays)
        d[p] = build_RayImpact_info(p,game,hitlist,angle_degree_list)

    return d
