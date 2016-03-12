from robosimnxt2 import *
import random
import numpy as np

angle_start, angle_stop, angle_step = -180,180-1,10

# les rayons affiches a l'ecran resteront tant qu'on appelle pas efface()
from sprite import DrawOnceSprite
DrawOnceSprite.lifespan = 1000

init('vide')


def sample_x_y_angle():
    sw,sh = taille_terrain()
    d = diametre_robot()
    x = np.random.random_sample()  * (sw - d-1)+d//2
    y = np.random.random_sample()  * (sh - d-1)+d//2
    a = np.random.random_integers(0,360)
    return int(x),int(y),a

def matele(coords=None,a=None,show=True):
    if coords != None and a != None:
        angle_list = [a+i for i in range(angle_start,angle_stop+1,angle_step)]
        distlist   = telemetre_coords_list(*coords,angle_list=angle_list,show_rays=show)
    elif coords == None and a == None:
        distlist = [telemetre(rel_angle=x) for x in range(angle_start,angle_stop+1,angle_step)]
    return map(int,distlist)



def uniform_monte_carlo(show=True):
    if show: efface()
    x,y,a = sample_x_y_angle()
    if show: circle(int(x),int(y),8)
    return (x,y,a),matele( (x,y) ,a,show)

def compare_distlists(l1,l2):
    l1 = np.array(l1)
    l2 = np.array(l2)
    return np.linalg.norm(l1 - l2,ord=1)

def compare_distlists_rotations(l1,l2):
    l1 = np.array(l1)
    l2 = np.array(l2)
    return min( np.linalg.norm(l1 - np.concatenate((l2[i:],l2[:i])),ord=1) for i in range(len(l2)) )

def generate_sorted_coords(n):
    robo_tele_list = matele()
    comp_list = []
    for i in range(n):
        (x,y,a),tl = uniform_monte_carlo(False)
        d = compare_distlists( robo_tele_list , tl )
        comp_list.append ( (x,y,a,d) )
    return sorted(comp_list,key=lambda x:x[3])


def generate_sorted_coords_nxt(n):
    nxt_list = [28, 27, 28, 29, 31, 82, 81, 79, 79, 78, 79, 79, 81, 118, 29, 27, 26, 25, 25, 25, 26, 28, 29, 38, 37, 37, 36, 37, 37, 38, 40, 30, 29, 28, 27, 28]
    nxt_list =  [147, 97, 96, 96, 98, 102, 32, 29, 28, 27, 27, 27, 27, 27, 28, 28, 22, 22, 21, 21, 21, 21, 22, 22, 24, 90, 89, 88, 87, 88, 89, 147, 147, 255, 97, 97]
    nxt_list.reverse()
    robo_tele_list = [cm2pix(x) for x in nxt_list]
    comp_list = []
    for i in range(n):
        (x,y,a),tl = uniform_monte_carlo(False)
        d = compare_distlists_rotations( robo_tele_list , simutele2nxt(tl,3) )
        comp_list.append ( (x,y,a,d) )
    return sorted(comp_list,key=lambda x:x[3])

def rotation(l,i=-6):
    assert isinstance(l,list)
    return l[i:]+l[:i]

def simutele2nxt(l,n=3):
    l2 = l*3
    return [int(min( l2[i-n:i+n] )) for i in range(len(l),len(l)*2)]

if __name__ == '__main__':
    for i in range(10):
        x,y,a,d = generate_sorted_coords_nxt(400)[0]
        circle(x,y)
    raw_input()


def find_best(nxt,simu):
    best_i,best_j,best_d=0,0,10000
    for i in range(3,10):
        for j in range(-13,13):
            x = np.linalg.norm(np.array(rotation(nxt,j))-np.array(simutele2nxt(simu,i)),ord=1)
            if x < best_d:
                best_d = x
                best_i = i
                best_j = j
    return best_i,best_j,best_d
