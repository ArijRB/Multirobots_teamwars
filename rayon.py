#cython: boundscheck=False, nonecheck=False,wraparound=False,initializedcheck=False,cdivision=True
#
# Note:
# Cython n'est pas indispensable pour ce code.
# S'il est installe, il s'executera plus vite. Sinon, ce sera en "pure python"

from math import pi,cos,sin
import numpy as np
import pygame

# Define the boolean cython_compiled which is true if compilation takes place
try:
    import cython
    cython_compiled = cython.compiled
except:
    cython_compiled = False


# bresenham algorithm cropped in the window (0,0,w,h)
def rayon(m,x,y,angle,w,h):
    """
        cette fonction lance un rayon, avec l'algo de bresenham
        le rayon part de (x,y) et suit un angle donne jusqu'au bord
        du carre (0,0,w,h)
        la fonction renvoie les coordonnees du premier point du masque qui soit a 1.
    """
    _cython_compiled = cython_compiled
    if _cython_compiled:    bm = cyGetBitmask(m)

    x2 = x + int( cos(angle)*(w+h) )
    y2 = y + int( sin(angle)*(w+h) )

    steep = 0
    dx = abs(x2 - x)
    dy = abs(y2 - y)
    if (x2 - x) > 0: sx = 1
    else: sx = -1

    if (y2 - y) > 0: sy = 1
    else: sy = -1

    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
        w,h   = h,w

    d = (2 * dy) - dx

    i = 0

    while x >= 0 and y >= 0 and x < w and y < h and i <= dx:
        if steep:
            if _cython_compiled:
                if cyBitmaskGetbit(bm,y,x) < 1:
                    return (y,x)
            else:
                if m.get_at((y,x)) < 1:
                    return (y,x)
        else:
            if _cython_compiled:
                if cyBitmaskGetbit(bm,x,y) < 1:
                    return (x,y)
            else:
                if m.get_at((x,y)) < 1:
                    return (x,y)

        while d >= 0:
            y = y + sy
            d = d - (2 * dx)

        x += sx
        d += 2 * dy
        i += 1
    return None

# Unit Test
def test_rayon():
    """
        ce test unitaire cree une image carre.png
        ou est affiche le contour d'un carre en pointille
    """
    import numpy as np
    import matplotlib.pyplot as plt

    im = pygame.image.load('Unused/DataUnused/Square.png')
    m = pygame.mask.from_surface(im)
    print "go..."

    T = np.zeros((256,256))
    w,h = im.get_width(),im.get_height()
    for angle in np.linspace(0,2*pi-0.1,50):
        T[  rayon(m,w/2,h/2,angle,w,h) ] = 1

    plt.imshow(T,cmap='gist_ncar')
    plt.savefig('carre.png')
