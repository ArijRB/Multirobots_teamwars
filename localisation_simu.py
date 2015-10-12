from robosimnxt2 import *
import random
import numpy as np

angle_start, angle_stop, angle_step = -180,180-1,30

# les rayons affiches a l'ecran resteront tant qu'on appelle pas efface()
from sprite import DrawOnceSprite
DrawOnceSprite.lifespan = 1000

init('robot_obstacles')


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

def generate_sorted_coords(n):
    robo_tele_list = matele()
    comp_list = []
    for i in range(n):
        (x,y,a),tl = uniform_monte_carlo(False)
        d = compare_distlists( robo_tele_list , tl )
        comp_list.append ( (x,y,a,d) )
    return sorted(comp_list,key=lambda x:x[3])

#for i in range(10):
#    x,y,a,d = generate_sorted_coords(400)[0]
#    circle(x,y)
#print(min(comp_list))
from robosim import position
#print(telemetre_coords_list(300,250,angle_list=[8+i for i in range(angle_start,angle_stop+1,angle_step)],show_rays=True))
print(telemetre_coords_list(*position(),angle_list=[0+i for i in range(angle_start,angle_stop+1,angle_step)],show_rays=True))
raw_input()
