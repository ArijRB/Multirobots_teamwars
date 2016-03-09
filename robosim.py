"""
Robosim Module
"""

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from sprite import MySprite,MovingSprite
from players import Player,Turtle
from spritebuilder import SpriteBuilder
import random
from math import pi,cos,sin,sqrt
import pygame
import glo
import pygame.draw


print("""\n---==[ Fonction disponibles ]==---""")
print("""init,avance,obstacle,oriente,\ntournegauche,tournedroite,telemetre,\ntelemetre_coords,position,orientation,diametre_robot,taille_terrain\nset_position,obstacle_coords\nline,circle,efface\npenup,pendown,color,frame_skip""")
print("""=[ Pour l'aide, tapez help(fonction) ]=\n""")


class TurtleSpriteBuilder(SpriteBuilder):
    def basicPlayerFactory(self,tileid=None,x=0.0,y=0.0):
        return Turtle("joueur",x,y,32,32)

###########################################

game = Game()

def init(_boardname=None,_spriteBuilder=TurtleSpriteBuilder):
    """
    Reinitialise la carte et l'ensemble des parametres
    """
    global player,game
    pygame.quit()

    name = _boardname if _boardname else 'robot_obstacles'
    game = Game('Cartes/' + name + '.json', _spriteBuilder)

    game.fps = 200  # frames per second
    game.mainiteration()
    player = game.player

    # new attributes
    game.pencolor = glo.RED
    game.usepen = False
    game.frame_skip = 0


@check_init_game_done
def frameskip(n):
    """
    frameskip(n) n'affichera qu'une image sur n.
    frameskip(0) affiche tout, et donc c'est assez lent.
    """
    game.frameskip = n


@check_init_game_done
def avance(s=1.0,p=None):
    """
    avance() deplace robot d'un pixel dans sa direction courante
    avance(x) le deplace de x pixels

    si dans x pixels il y a un obstacle, alors le deplacement echoue,
    et le robot reste a sa position courante et la fonction renvoie False.
    S'il n'y a pas d'obstacle la fonction renvoie True
    """
    p = player if p is None else p
    cx1,cy1 = p.get_centroid()
    p.forward(s)
    game.mainiteration()
    if p.position_changed():
        if game.usepen:
            cx2,cy2 = p.get_centroid()
            line(cx1,cy1,cx2,cy2)
        return True
    else:
        return False

@check_init_game_done
def obstacle(s=1.0,p=None):
    """
    obstacle(x) verifie si un obstacle empeche le deplacement du robot de x pixel dans sa direction courante
    obstacle()  verifie la meme chose pour un deplacement de un pixel
    """
    p = player if p is None else p
    p.forward(s)
    game.mask.handle_collision(game.layers, p)

    if p.resumed:
        return True
    else:
        p.resume_to_backup()
        return False

@check_init_game_done
def oriente(a,p=None):
    """
    oriente(a) fait pivoter le robot afin qu'il forme un angle de a degrees
    par rapport a l'horizontal.
    Donc oriente(0) le fait se tourner vers l'Est
    Donc oriente(90) le fait se tourner vers le Sud
    Donc oriente(-90) le fait se tourner vers le Nord
    Donc oriente(180) le fait se tourner vers l'Ouest
    """
    p = player if p is None else p
    p.translate_sprite(p.x,p.y,a,relative=False)
    game.mainiteration()

@check_init_game_done
def tournegauche(a,p=None):
    """
    tournegauche(a) pivote d'un angle donne, en degrees
    """
    p = player if p is None else p
    p.translate_sprite(0,0,-a,relative=True)
    game.mainiteration()

@check_init_game_done
def tournedroite(a,p=None):
    """
    tournedroite(a) pivote d'un angle a donne, en degrees
    """
    p = player if p is None else p
    p.translate_sprite(0,0,a,relative=True)
    game.mainiteration()

@check_init_game_done
def telemetre(from_center=False,rel_angle=0,p=None):
    """
    telemetre(from_center=False,rel_angle=0)

    telemetre() tire un rayon laser dans la direction du robot
    la fonction renvoie le nombre de pixels que le robot peut parcourir avant
    de rencontrer un obstacle.
    telemetre(from_center=True) compte le nombre de pixels depuis le centre du robot (et non pas le bord)
    telemetre(rel_angle) tire le rayon avec l'angle rel_angle (relativement a l'orientation du robot)
    """
    p = player if p is None else p
    rayon_hit = p.throw_rays([(p.angle_degree+rel_angle)*pi/180] , game.mask,game.layers,show_rays=True)[0]
    game.mainiteration()
    d = p.dist(*rayon_hit)
    return d if from_center else d-(diametre_robot()//2)

@check_init_game_done
def telemetre_coords_list(x,y,angle_list,show_rays=True,p=None):
    """
    telemetre_coords_list(x,y,angle_list,show_rays=True)
    tire un rayon laser depuis x,y avec les angles angle_list
    la fonction renvoie une liste contenant les nombres de pixels parcourus par le rayon avant
    de rencontrer un obstacle
    """
    p = player if p is None else p
    x,y = int(x),int(y)
    hitlist = p.throw_rays([a*pi/180 for a in angle_list] , game.mask,game.layers,coords=(x,y),show_rays=show_rays)
    game.mainiteration()
    return [sqrt( (rx-x)**2 + (ry-y)**2 ) for rx,ry in hitlist]

@check_init_game_done
def telemetre_coords(x,y,a):
    """ voir telemetre_coords_list """
    return telemetre_coords_list(x,y,[a])[0]

@check_init_game_done
def position(entiers=False,p=None):
    """
    position() renvoie un couple (x,y) representant les coordonnees du robot
               ces coordonnees peuvent etre des flottants
    position(entiers=True) renvoie un couple de coordonnees entieres
    """
    p = player if p is None else p
    cx,cy = p.get_centroid()
    return (int(cx),int(cy)) if entiers else (cx,cy)

@check_init_game_done
def diametre_robot(p=None):
    p = player if p is None else p
    return p.taille_geometrique

@check_init_game_done
def taille_terrain():
    return game.screen.get_width(),game.screen.get_height()

@check_init_game_done
def orientation(p=None):
    """
    orientation() renvoie l'angle en degres
    """
    p = player if p is None else p
    return p.angle_degree

@check_init_game_done
def set_position(x,y,p=None):
    """
    set_position(x,y) tente une teleportation du robot aux coordonnees x,y
    Renvoie False si la teleportation a echouee, pour cause d'obstacle
    """
    p = player if p is None else p
    p.set_centroid(x,y)
    game.mainiteration()
    return p.position_changed()

@check_init_game_done
def obstacle_coords(x,y,p=None):
    """
    obstacle_coords(x,y) verifie si aux coordonnees x,y il y a un
    obstacle qui empecherait le robot d'y etre
    renvoie True s'il y a un obstacle, False sinon
    """
    p = player if p is None else p
    p.set_centroid(x,y)
    game.mask.handle_collision(game.layers, p)

    #if player.position_changed():
    if p.resumed:
        return True
    else:
        p.resume_to_backup()
        return False

@check_init_game_done
def line(x1,y1,x2,y2,wait=False):
    """
    line(x1,y1,x2,y2,wait=False) dessine une ligne de (x1,y1) a (x2,y2)
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    game.prepare_dessinable()
    pygame.draw.aaline(game.surfaceDessinable, game.pencolor, (int(x1),int(y1)), (int(x2),int(y2)))
    if not wait:
        game.mainiteration()

@check_init_game_done
def circle(x1,y1,r=10,wait=False):
    """
    circle(x,y,r) dessine un cercle
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    game.prepare_dessinable()
    pygame.draw.circle(game.surfaceDessinable, game.pencolor, (int(x1),int(y1)), r)
    if not wait:
        game.mainiteration()

@check_init_game_done
def efface():
    """
    efface() va effacer tous les dessins
    """
    game.kill_dessinable()
    game.mainiteration()


@check_init_game_done
def color(c):
    """
    color(c) change la couleur du dessin.
    par exemple, pour avoir du bleu, faire color((0,255,0))
    Attention, il y a un bug: la couleur bleue ne fonctionne pas
    """
    game.pencolor = c

@check_init_game_done
def pendown():
    """
    pendown() abaisse le stylo
    """
    game.usepen = True

@check_init_game_done
def penup():
    """
    penup() releve le stylo
    """
    game.usepen = False


av, tele, setheading, tg, td, pos, teleporte  = avance, telemetre, oriente, tournegauche, tournedroite, position, set_position
