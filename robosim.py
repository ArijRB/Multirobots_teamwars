from gameclass import Game
from sprite import MySprite,MovingSprite
from players import Player,Turtle
from spritebuilder import SpriteBuilder
import random
from math import pi,cos,sin
import pygame
import glo
from functools import wraps

class TurtleSpriteBuilder(SpriteBuilder):
    def basicSpriteFactory(self,spritegroups , layername,tileid,x,y,img):
        if layername == "joueur":
            j = Turtle(layername,tileid,x,y,[img])
            spritegroups[layername].add( j )
            j.build_dessin()
        else:
            SpriteBuilder.basicSpriteFactory(spritegroups,layername,tileid,x,y,img)

###########################################

class gw:
    game = None
    fps = None
    name = 'robot_obstacles'


def init(_boardname=None):
    global player
    pygame.quit()
    if _boardname: gw.name = _boardname
    gw.fps = 60  # frames per second
    gw.game = Game('Cartes/' + gw.name + '.json', TurtleSpriteBuilder)
    gw.game.mainiteration(60)
    player = gw.game.player


def check_init_done(fun):
    """ decorator checking if init() has correctly been called before anything """
    @wraps(fun  )
    def fun_checked(*args):
        try:
            return fun(*args)
        except NameError:
            print("Erreur: appeler la fonction init() avant toute chose")
    return fun_checked

@check_init_done
def avance(s=1.0):
    """
    avance() deplace robot d'un pixel dans sa direction courante
    avance(x) le deplace de x pixels

    si dans x pixels il y a un obstacle, alors le deplacement echoue,
    et le robot reste a sa position courante et la fonction renvoie False.
    S'il n'y a pas d'obstacle la fonction renvoie True
    """
    player.forward(s)
    gw.game.mainiteration()
    return player.position_changed()

@check_init_done
def obstacle(s=1.0):
    """
    obstacle(x) verifie si un obstacle empeche le deplacement du robot de x pixel dans sa direction courante
    obstacle()  verifie la meme chose pour un deplacement de un pixel
    """
    player.forward(s)
    gw.game.mask.handle_collision(gw.game.groupDict, player)

    if player.resumed:
        return True
    else:
        player.resume_to_backup()
        return False

@check_init_done
def oriente(a):
    """
    oriente(a) fait pivoter le robot afin qu'il forme un angle de a degrees
    par rapport a l'horizontal.
    Donc oriente(0) le fait se tourner vers l'Est
    Donc oriente(90) le fait se tourner vers le Sud
    Donc oriente(-90) le fait se tourner vers le Nord
    Donc oriente(180) le fait se tourner vers l'Ouest
    """
    player.translate_sprite(player.x,player.y,a,relative=False)
    gw.game.mainiteration()

@check_init_done
def tournegauche(a):
    """
    pivote d'un angle donne, en degrees
    """
    player.translate_sprite(0,0,-a,relative=True)
    gw.game.mainiteration()

@check_init_done
def tournedroite(a):
    """
    pivote d'un angle donne, en degrees
    """
    player.translate_sprite(0,0,a,relative=True)
    gw.game.mainiteration()

@check_init_done
def telemetre():
    """
    tire un rayon laser dans la direction courante.
    la fonction renvoie le nombre de pixels parcourus par le rayon avant
    de rencontrer un obstacle
    """
    rayon_hit = player.throw_ray(player.angle_degree*pi/180 , gw.game.mask,gw.game.groupDict)
    gw.game.mainiteration()
    return player.dist(*rayon_hit)

@check_init_done
def position():
    """
    renvoie un couple (x,y) representant les coordonnees du robot
    """
    return player.get_centroid()

@check_init_done
def set_position(x,y):
    """
    Tente une teleportation du robot aux coordonnees x,y
    Renvoie False si la teleportation a echouee, pour cause d'obstacle
    """
    player.set_centroid(x,y)
    gw.game.mainiteration()
    return player.position_changed()

@check_init_done
def obstacle_coords(x,y):
    """
    verifie si aux coordonnees x,y il y a un obstacle qui empecherait
    le robot d'y etre
    renvoie True s'il y a un obstacle, False sinon
    """
    player.set_centroid(x,y)
    gw.game.mask.handle_collision(gw.game.groupDict, player)

    #if player.position_changed():
    if player.resumed:
        return True
    else:
        player.resume_to_backup()
        return False

av, tele, setheading, tg, td, pos, teleporte  = avance, telemetre, oriente, tournegauche, tournedroite, position, set_position
