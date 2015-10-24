from robosim import *
import numpy as np
import math
from evo_strategy import *

init()

def cosd(x): return math.cos(x*math.pi/180.0)
def sind(x): return math.sin(x*math.pi/180.0)

angle_start, angle_stop, angle_step = -90,90,45

def teleVectors():
    """
    renvoie une liste de vecteurs 2D
    ces vecteurs representent le point d'intersection entre le rayon telemetrique et les obstacles
    ces vecteurs sont dans le repere du robot.
    donc un vecteur (10,10) represente vecteur a 45 degres de l'orientation du robot, de norme 10*sqrt(2)
    """
    angles = range(angle_start,angle_stop+1,angle_step)
    x,y = position()
    def _telemetre(rel_angle):
        return telemetre_coords_list(x,y,[rel_angle+orientation()],show_rays=False)[0]-diametre_robot()//2
    distlist = [_telemetre(rel_angle=a) for a in angles]
    vec = [np.array([d*cosd(a),d*sind(a)]) for d,a in zip(distlist,angles)]
    return vec

def compute_weight(d,theta):
    """ renvoie la nouvelle norme d'un vecteur en fonction de son ancienne norme
    """
    assert len(theta)==2
    return theta[0]-1.0/(1.0+d*theta[1])

def compute_heading(vecs,theta):
    #i = np.argmax( [np.linalg.norm(v) for v in vecs] )
    #return int( np.arctan2(vecs[i][1],vecs[i][0])*180.0/math.pi )
    s = np.zeros(2)
    for v in vecs:
        assert isinstance(v,np.ndarray)
        n = np.linalg.norm(v)
        if n > 0.001:
            w = compute_weight(n,theta) / n
            s += v * w
    return int(np.arctan2(s[1],s[0])*180.0/math.pi)

av(10)
initial_position = position()
initial_orientation = orientation()

theta_glob = np.array([1.0,1.0])

def va_vers_max_telemetre():
    while True:
        vecs = teleVectors()
        td( compute_heading(vecs,theta_glob) )
        av()

def evalueTheta(theta):
    set_position(*initial_position)
    oriente(initial_orientation)
    for i in range(100):
        vecs = teleVectors()
        td( compute_heading(vecs,theta) )
        av(5)
    cx,cy = position()
    return cx+cy


def optimise_theta():
    frameskip(100)
    best_theta = optim(N=2,f=evalueTheta,niter=2000,verb=True)
    frameskip(0)
    print "meilleur theta = ",best_theta
    print "appuyez sur une touche pour voir la trajectoire"
    raw_input()
    evalueTheta(best_theta)

#optimise_theta()
evalueTheta([ 0.5,0.5])
raw_input()
evalueTheta([ 0.02649329 , 1.25210125])
