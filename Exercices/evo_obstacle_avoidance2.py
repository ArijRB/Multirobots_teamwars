from random import gauss
from robosim import *
"""  bon jeu de donnees:
     [27.27478041063894, 0.9145028448306789, 44.45127808968659, -163.01108685787582, -2.563960274704059]
"""
def optim(f,N,niter):
    Lbest = [5.0]*N
    for c in range(niter):
        L = []
        sigma = (30 if c < niter//2 else 5)
        for x in Lbest:
            L.append( x+ gauss(0,1)*sigma )

        if f(L) < f(Lbest):
        	Lbest = L
    return Lbest


def test_optim():
    """ test de la fonction optim """
    def f(L): return (L[0]-3.0)**2+(L[1]-4.0)**2
    x , y = optim(f,2,1000)
    print x,y


def teleangle(a):
    td(a)
    d = telemetre()
    tg(a)
    return d

def teleangle_rapide(a):
    """ meme chose que teleangle, mais en plus rapide """
    return telemetre_coords_list(*position(),angle_list=[a],show_rays=False)[0] - diametre_robot()//2


def evitement(x1,x2,x3,x4,x5):
    if teleangle_rapide(0) < x1:
        tg(180)
    elif teleangle_rapide(-60) < x2:
        td(x3)
    elif teleangle_rapide(60) > x4:
        tg(x5)
    avance(5)

def evalue_parametres(L):
    set_position(144,112)
    oriente(0)
    for i in range(150):
        evitement(*L)
        if obstacle(5):
            break
    x,y = position()
    return abs(512-x)+abs(512-y)

def optim_evitement():
    init()
    frameskip(100)
    return optim( evalue_parametres , 5 , 1000 )

Lbest = optim_evitement()
frameskip(0)
evalue_parametres(Lbest)
print Lbest
