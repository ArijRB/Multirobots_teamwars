from robosim import *
from correction_info2_tp3 import init_graph,draw_graph, suivre_chemin
from math import cos,sin,pi,sqrt
from operator import itemgetter
import networkx as nx
from time import time

def octant(x,y):
    """ Renvoie l'angle parmi [0,45,90,135,180,-135,-90,-45]
        s'orientant vers (x,y)
        Les angles 0,90,180,-90 ne sont choisis que si cx=x ou cy=y
    """
    cx,cy = position(entiers=True)

    if y == cy:
        # 0, 180
        return 0 if x >= cx else 180

    s = 1 if y > cy else -1

    if x == cx:
        return s*90
    else:
        return s*45 if x > cx else s*135


def aller(x,y):
    """
    Cette fonction generalise la fonction aller(x,y) ecrite au TP3
    Le robot se deplace et arrive exactement en (x,y), quelque soit (x,y)
    s'il croise un obstacle il s'arrete et renvoie False
    """
    cx,cy = position(entiers=True)

    while x != cx or y != cy:
        oriente(octant(x,y))
        if not av():
            return False
        cx,cy = position(entiers=True)
    return True


def testArete(G,d):
    """ le robot est un cercle de diametre 22
        il faut qu'il puisse avancer le long d'un couloir de taille 30 (petite marge de securite)
        et le couloir peut etre long de d pixels
    """
    angle_initial = orientation()
    td(90)
    for i in range(0,181,10):
        a = i*pi/180.0
        r = telemetre()
        x,y = r*cos(a) , r*sin(a)
        if -15 <= x <= 15 and 0 <= y <= d+5:
            oriente(angle_initial)
            return False
        tg(10)
    oriente(angle_initial)
    return True

def effaceLesAretesBloquees(G,K):
    """ renvoie vrai si au moins une arete a ete supprimee
    """
    x,y = position(entiers=True)
    assert (x,y) in G
    changed = False

    for x2,y2 in G.neighbors( (x,y) ):
        oriente(octant(x2,y2))
        d = sqrt( (x2-x)**2 + (y2-y)**2 )
        if not testArete(G,d) and not (x2,y2) in K:
            G.remove_edge( (x2,y2),(x,y) )
            changed = True
    return changed

def main_algorithm(G,exploration_strategy):
    K = set()
    p = position(entiers=True)

    while len(K) < len(nx.node_connected_component(G,p)):
        p = position(entiers=True)
        if p not in K:
            if effaceLesAretesBloquees(G,K):
                draw_graph(G)
            K.add( p )
        exploration_strategy(G,K)

def explore_random(G,K):
    """ explores randomly, but selects unknown states if there are some"""
    N = set(G.neighbors( position(entiers=True) ))

    if len(N-K) > 0:
        (x2,y2) = random.choice( list(N-K) )
    else:
        (x2,y2) = random.choice( list(N) )

    aller(x2,y2)

def explore_shortestpath(G,K):
    cx,cy = position(entiers=True)
    _ , dist = nx.dijkstra_predecessor_and_distance( G,(cx,cy) )
    dist = {ij:dist[ij] for ij in dist if ij not in K}
    if dist:
        closest, _ = min(dist.items(), key=itemgetter(1))
        p = nx.shortest_path(G,(cx,cy),closest,weight='weight')
        suivre_chemin(p,aller)

def main():
    init('robot_obstacles_invisibles')
    frameskip(60) # affiche une image sur n pour acceler la simulation
    print "Premiere strategie d'exploration: aleatoire guidee"
    debut1 = time()
    G = init_graph(80,440,30)
    teleporte(80,80)
    draw_graph(G)
    #main_algorithm(G,explore_random)
    print "Temps d'exploration = ",time()-debut1,"secondes\n"
    print "deuxieme strategie d'exploration: shortest path"
    debut2 = time()
    G = init_graph(80,440,30)
    teleporte(80,80)
    draw_graph(G)
    main_algorithm(G,explore_shortestpath)
    print "Temps d'exploration = ",time()-debut2,"secondes\n"

if __name__ == '__main__':
    main()
