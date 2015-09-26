from robosim import *
from correction_info2_tp3 import init_graph,draw_graph, prune_nodes, aller, suivre_chemin
from math import cos,sin,pi

def testArete(G,d):
    """ le robot est un cercle de diametre 22
        il faut qu'il puisse avancer le long d'un couloir de taille 24 (petite marge de securite)
        et le couloir peut etre long de d pixels
    """
    td(90)
    dist = []
    for i in range(0,180,5):
        a = i*pi/180.0
        r = telemetre()
        x,y = r*cos(a) , r*sin(a)
        if -12 <= x <= 12 and 0 <= y <= d:
            return False
        tg(5)
    return True



if __name__ == '__main__':
