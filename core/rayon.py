#cython: boundscheck=False, nonecheck=False,wraparound=False,initializedcheck=False,cdivision=True
#
# Note:
# Cython n'est pas indispensable pour ce code.
# S'il n'est pas installe, il s'executera en python simple.
# S'il est installe, alors il faut d'abord compiler ce fichier avec la commande:
#   python setup.py build_ext --inplace
# puis cython sera utilise par defaut
#
# Speed test sur l'image square2.png, le rayon parcourt 200 pixels avant de s'arreter
# avec Cython actif,     un appel a rayon prend: 2.24 microsec per loop
# avec seulement Python, un appel a rayon prend: 188 microsec per loop

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
def rayon(m1,m2,x,y,angle_degree,w,h,max_radius):
    """
        cette fonction lance un rayon, avec l'algo de bresenham
        le rayon part de (x,y) et suit un angle donne jusqu'au bord
        du carre (left,top,right,bottom)
        la fonction renvoie les coordonnees du premier point du masque qui soit a 1.
    """
    _cython_compiled = cython_compiled
    if _cython_compiled:
        bm1 = cyGetBitmask(m1)
        bm2 = cyGetBitmask(m2)

    if max_radius is None: max_radius = w+h

    x2 = x + int( cos(angle_degree*3.14159/180.0)*max_radius )
    y2 = y + int( sin(angle_degree*3.14159/180.0)*max_radius )
    x,y = int(x),int(y)
    w,h = int(w),int(h)


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
        w,h = h,w

    d = (2 * dy) - dx

    i = 0

    # boucle principale de l'algo de Bresenham
    while y >= 0 and 0 <= x < w and y < h and i <= dx:
        if steep:
            #print y,x
            if _cython_compiled:
                if cyBitmaskGetbit(bm1,y,x) or cyBitmaskGetbit(bm2,y,x):
                    return (y,x)
            else:
                if m1.get_at((y,x)) or m2.get_at((y,x)):
                    return (y,x)
        else:
            #print x,y
            if _cython_compiled:
                if cyBitmaskGetbit(bm1,x,y) or cyBitmaskGetbit(bm2,x,y):
                    return (x,y)
            else:
                if m1.get_at((x,y)) or m2.get_at((x,y)):
                    return (x,y)

        while d >= 0:
            y += sy
            d = d - (2 * dx)

        x += sx
        d += 2 * dy
        i += 1
    return (y,x) if steep else (x,y) # or None ?







# Unit Test
def test_rayon():
    """
        ce test unitaire charge une image Square2.png
        et cree une image carre.png
        ou est affiche le contour du carre en pointille
    """
    import numpy as np
    import matplotlib.pyplot as plt

    im = pygame.image.load('Unused/DataUnused/Square2.png')
    m = pygame.mask.from_surface(im)
    w,h = im.get_width(),im.get_height()
    print ("Unit test launched...")

    T = np.zeros((w,h))
    for angle in np.linspace(0,360,50):
        T[ rayon(m,m,w/2,h/2,angle,w,h,max_radius=None) ] = 1

    plt.imshow(T,cmap='gist_ncar')
    plt.savefig('carre.png')
    print ("image file carre.png should have a dotted square")

if __name__ == '__main__':
    test_rayon()
