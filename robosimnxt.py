from robosim import (
    rs,
    init as robosim_init,
    tg as robosim_tg,
    td as robosim_td,
    check_init_done,
    frameskip,
    avance as robosim_avance,
    av as robosim_av,
    obstacle,
    oriente,
    telemetre,
    telemetre_coords,
    position,
    orientation,
    set_position,
    obstacle_coords,
    line,
    circle,
    efface,
    color,
    pendown,
    penup,
    tele, setheading, pos, teleporte
    )

import thread, time
from math import pi,floor
import random

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
    assert rs.game.screen.get_width() == rs.game.screen.get_height() ,"le terrain sur l'ecran devrait etre carre et non rectangulaire"

def pix2cm(p): return p * taille_board_cm / rs.game.screen.get_width()
def cm2pix(c): return rs.game.screen.get_width() * c / taille_board_cm
def randround(x): return int(floor(x) + (0 if random.random() > (x-floor(x)) else 1))

def const_unicycle_sim(degrees):
    # Command to the Turtle
    cm = 18
    pix = cm2pix(cm)
    pix = randround(pix)
    degrees = int( degrees+ random.gauss(0,abs(degrees)/20.0) )
    real_pix = 0.0
    if pix == 0:
        robosim_td(degrees)
    else:
        for i in range( pix ):
            robosim_td(degrees*1.0 / pix)
            if robosim_av():
                real_pix += 1.0

    return degrees

def const_unicycle_nxt(degrees):
    #assert cm >= 10.0 , "avancer le nxt d'au moins 10 cm"
    cm = 18.0

    deg = int( abs(degrees) * 35.0/45 )
    if degrees < 0:
        both = nxt.SynchronizedMotors(nxt_mG, nxt_mD, deg)
    else:
        both = nxt.SynchronizedMotors(nxt_mD,nxt_mG, deg)

    both.turn(nxt_sens_moteurs*85, 360, False)


def const_unicycle(degrees):
    c,d = unicycle_sim(cm,degrees)
    if 'nxt' in globals() and 'nxt_b' in globals():
        return unicycle_nxt(cm,degrees)
    else:
        return c,d
