from robosim import (
    game,
    init as robosim_init,
    tg as robosim_tg,
    td as robosim_td,
    check_init_game_done,
    frameskip,
    avance as robosim_avance,
    obstacle,
    oriente,
    telemetre,
    telemetre_coords,
    telemetre_coords_list,
    set_position,
    obstacle_coords,
    line,
    circle,
    efface,
    color,
    pendown,
    penup,
    taille_terrain,
    diametre_robot,
    tele, setheading, pos, teleporte
    )

import thread, time
from math import pi,floor
import random
import pygame
import glo
from sprite import *

try:
    import nxt
    nxt_port_tourelle      = nxt.PORT_A # tourelle
    nxt_port_moteur_gauche = nxt.PORT_B # Gauche, fixe a l'envers
    nxt_port_moteur_droit  = nxt.PORT_C # Droite, fixe a l'envers
    nxt_sens_moteurs       = -1 # sens des moteurs gauche et droit
    nxt_port_ultrason      = nxt.PORT_4
    nxt_ecart_roues = 15.5 #cm
    nxt_circonference_roues = 13.5 #cm
except:
    pass

taille_board_cm = 120.0 #cm


def avance(n):
    bruit = randround( random.gauss(0,n/20) )
    return robosim_avance(n+bruit)

def tournegauche(n):
    assert n in [0,30,60,90], "les angles passes a td() et tg() doivent etre un multiple de 30"
    bruit = randround( random.gauss(0,n/20) )
    return robosim_tg(n+bruit)

def tournedroite(n):
    assert n in [0,30,60,90], "les angles passes a td() et tg() doivent etre un multiple de 30"
    bruit = randround( random.gauss(0,n/20) )
    return robosim_td(n+bruit)

av , tg, td = avance,tournegauche,tournedroite





def init_nxt():
    global nxt_b,nxt_mT,nxt_mG,nxt_mD,nxt_ultrason,nxt_both,nxt_leftboth,nxt_rightboth

    # was 'find_one_brick' already called and stored in 'nxt_b' ?
    if 'nxt_b' not in globals():
        try:
            nxt_b = nxt.find_one_brick()
        except nxt.locator.BrickNotFoundError:
            print("Attention: la brique du NxT n'a pas ete trouvee")
            return False

    nxt_mT = nxt.Motor(nxt_b, nxt_port_tourelle)
    nxt_mG = nxt.Motor(nxt_b, nxt_port_moteur_gauche)
    nxt_mD = nxt.Motor(nxt_b, nxt_port_moteur_droit)
    nxt_ultrason = nxt.sensor.Ultrasonic(nxt_b,nxt_port_ultrason)

    nxt_both = nxt.SynchronizedMotors(nxt_mG, nxt_mD, 0)
    nxt_leftboth = nxt.SynchronizedMotors(nxt_mG, nxt_mD, 100)
    nxt_rightboth = nxt.SynchronizedMotors(nxt_mD, nxt_mG, 100)
    return True

def get_nxt():
    """ renvoie un tuple contenant:
    la brique, le moteur tourelle, le moteur gauche, le moteur droit, le capteur Ultrason
    """
    return (nxt_b,nxt_mT,nxt_mG,nxt_mD,nxt_ultrason)

def init(_boardname=None):
    # did we import the nxt module ?
    if 'nxt' in globals():
        init_nxt()
    robosim_init(_boardname)
    assert game.screen.get_width() == game.screen.get_height() ,"le terrain sur l'ecran devrait etre carre et non rectangulaire"

    if _boardname== 'vide':
        big_obstacle = pygame.Surface([game.screen.get_width(), game.screen.get_height()]).convert()
        big_obstacle.set_colorkey( (0,0,0) )
        larg,haut=cm2pix(39),cm2pix(30)
        px , py  =cm2pix(20),cm2pix(20)
        r = pygame.Rect(512-px-larg,512-py-haut,larg,haut)
        pygame.draw.rect( big_obstacle,glo.BLUE, r)
        game.layers['obstacle'].add( MySprite('obstacle',None,0,0,[big_obstacle]) )
        set_position(cm2pix(32),512-cm2pix(40)) # 60 cm du bord, au milieu
        av(1)

def pix2cm(p): return p * taille_board_cm / game.screen.get_width()
def cm2pix(c): return game.screen.get_width() * c / taille_board_cm
def randround(x): return int(floor(x) + (0 if random.random() > (x-floor(x)) else 1))
