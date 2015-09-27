from gameclass import Game
from sprite import MySprite,MovingSprite
from players import Player,Turtle
from spritebuilder import SpriteBuilder
import random
from math import pi,cos,sin,sqrt
import pygame
import glo
from functools import wraps
import pygame.draw


print("""\n---==[ Fonction disponibles ]==---""")
print("""init,avance,obstacle,oriente,\ntournegauche,tournedroite,telemetre,\ntelemetre_coords,position,orientation\nset_position,obstacle_coords\nline,circle,efface\npenup,pendown,color,turn_screen_update""")
print("""=[ Pour l'aide, tapez help(fonction) ]=\n""")


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
    pass

def init(_boardname=None):
    """
    Reinitialise la carte et l'ensemble des parametres
    """
    global player
    pygame.quit()

    gw.name = 'robot_obstacles'
    gw.pencolor = glo.RED
    gw.usepen = False
    gw.fps = 200  # frames per second
    if _boardname: gw.name = _boardname
    gw.game = Game('Cartes/' + gw.name + '.json', TurtleSpriteBuilder)
    gw.game.mainiteration(gw.fps)
    player = gw.game.player
    gw.always_update_screen = True


def check_init_done(fun):
    """ decorator checking if init() has correctly been called before anything """
    @wraps(fun  )
    def fun_checked(*args,**kwargs):
        try:
            gw.game
        except AttributeError:
            print("Erreur: appeler la fonction init() avant toute chose")
        else:
            return fun(*args,**kwargs)
    return fun_checked

@check_init_done
def turn_screen_update(on_off):
    """
    Call turn_screen_update('on') to prevent refreshing the screen
    This will speed up the simulation
    """
    assert on_off in ['on','off']
    gw.always_update_screen = (on_off=='on')


@check_init_done
def avance(s=1.0):
    """
    avance() deplace robot d'un pixel dans sa direction courante
    avance(x) le deplace de x pixels

    si dans x pixels il y a un obstacle, alors le deplacement echoue,
    et le robot reste a sa position courante et la fonction renvoie False.
    S'il n'y a pas d'obstacle la fonction renvoie True
    """
    cx1,cy1 = player.get_centroid()
    player.forward(s)
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)
    if player.position_changed():
        if gw.usepen:
            cx2,cy2 = player.get_centroid()
            line(cx1,cy1,cx2,cy2)
        return True
    else:
        return False

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
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)

@check_init_done
def tournegauche(a):
    """
    tournegauche(a) pivote d'un angle donne, en degrees
    """
    player.translate_sprite(0,0,-a,relative=True)
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)

@check_init_done
def tournedroite(a):
    """
    tournedroite(a) pivote d'un angle a donne, en degrees
    """
    player.translate_sprite(0,0,a,relative=True)
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)

@check_init_done
def telemetre():
    """
    telemetre() tire un rayon laser dans la direction courante.
    la fonction renvoie le nombre de pixels parcourus par le rayon avant
    de rencontrer un obstacle
    """
    rayon_hit = player.throw_ray(player.angle_degree*pi/180 , gw.game.mask,gw.game.groupDict)
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)
    return player.dist(*rayon_hit)-(player.taille_geometrique//2)

@check_init_done
def telemetre_coords(x,y,a):
    """
    telemetre_coords(x,y,a,display=True)
    tire un rayon laser depuis x,y avec l'angle a
    la fonction renvoie le nombre de pixels parcourus par le rayon avant
    de rencontrer un obstacle
    """
    rx,ry = player.throw_ray(a*pi/180 , gw.game.mask,gw.game.groupDict,coords=(x,y))
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen)

    return sqrt( (rx-x)**2 + (ry-y)**2 )

@check_init_done
def position(entiers=False):
    """
    position() renvoie un couple (x,y) representant les coordonnees du robot
               ces coordonnees peuvent etre des flottants
    position(entiers=True) renvoie un couple de coordonnees entieres
    """
    cx,cy = player.get_centroid()
    return (int(cx),int(cy)) if entiers else (cx,cy)

@check_init_done
def orientation():
    """
    orientation() renvoie l'angle en degres
    """
    return player.angle_degree

@check_init_done
def set_position(x,y):
    """
    set_position(x,y) tente une teleportation du robot aux coordonnees x,y
    Renvoie False si la teleportation a echouee, pour cause d'obstacle
    """
    player.set_centroid(x,y)
    gw.game.mainiteration(gw.fps,gw.always_update_screen)
    return player.position_changed()

@check_init_done
def obstacle_coords(x,y):
    """
    obstacle_coords(x,y) verifie si aux coordonnees x,y il y a un
    obstacle qui empecherait le robot d'y etre
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

@check_init_done
def line(x1,y1,x2,y2,wait=False):
    """
    line(x1,y1,x2,y2,wait=False) dessine une ligne de (x1,y1) a (x2,y2)
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    gw.game.prepare_dessinable()
    pygame.draw.aaline(gw.game.surfaceDessinable, gw.pencolor, (x1,y1), (x2,y2))
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen and not wait)

@check_init_done
def circle(x1,y1,r=10,wait=False):
    """
    circle(x,y,r) dessine un cercle
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    gw.game.prepare_dessinable()
    pygame.draw.circle(gw.game.surfaceDessinable, gw.pencolor, (x1,y1), r)
    gw.game.mainiteration(gw.fps,display= gw.always_update_screen and not wait)

@check_init_done
def efface():
    """
    efface() va effacer tous les dessins
    """
    gw.game.kill_dessinable()
    gw.game.mainiteration(gw.fps,gw.always_update_screen)


@check_init_done
def color(c):
    """
    color(c) change la couleur du dessin.
    par exemple, pour avoir du bleu, faire color((0,255,0))
    Attention, il y a un bug: la couleur bleue ne fonctionne pas
    """
    gw.pencolor = c

@check_init_done
def pendown():
    """
    pendown() abaisse le stylo
    """
    gw.usepen = True

@check_init_done
def penup():
    """
    penup() releve le stylo
    """
    gw.usepen = False


av, tele, setheading, tg, td, pos, teleporte  = avance, telemetre, oriente, tournegauche, tournedroite, position, set_position
