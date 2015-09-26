from robosim import *
import networkx as nx
from math import sqrt
import time

def first(gen): return list(gen)[0]
def last(gen):  return list(gen)[-1]

xstart = 80
xstop  = 440
gap    = 30


def init_graph( xstart,xstop,gap ):
    assert (xstop-xstart) % gap == 0, "xstop-xstart doit etre un multiple de gap"
    gen = range(xstart,xstop+1,gap)
    g = nx.Graph()

    for i in gen:
        for j in gen:
            if i > xstart and j < xstop:
                g.add_edge( (i,j),(i-gap,j+gap),weight=1.0)
            if j < xstop:
                g.add_edge( (i,j),(i,j+gap),weight=1.0)
            if i < xstop:
                g.add_edge( (i,j),(i+gap,j),weight=1.0)
            if j < xstop and i < xstop:
                g.add_edge( (i,j),(i+gap,j+gap),weight=1.414)
    return g

def draw_graph(g):
    efface()
    for (i1,j1),(i2,j2) in g.edges():
        # wait=True retarde l'affichage
        line(i1,j1,i2,j2,wait=True)
    line(0,0,0,0,wait=False) # juste pour lancer l'affichage de tout ce qui a ete differe


def prune_nodes(g):
    for i,j in g.nodes():
        if obstacle_coords(i,j):
            g.remove_node( (i,j) )

    #for (i1,j1),(i2,j2) in g.edges():
    #    if  i1 != i2 and j1 != j2 and not g.has_edge( (i1,j2),(i2,j1) ):
    #        g.remove_edge( (i1,j1),(i2,j2) )


def aller(x,y):
    """
    le robot se deplace direction Est/Sud/Sud-Est et arrive exactement en (x,y)
    La position du robot peut etre flottant. par exemple (80.3,29.7)
    du coup, le robot va devoir avancer au sous-pixel pres pour atteindre (x,y)
    """
    cx,cy = position()

    oriente(45)
    while (cx+1) < x and (cy+1) < y:
        av(1)
        cx,cy = position()

    oriente(0)
    while cx < x:
        av( min(1,x-cx) )
        cx,cy = position()

    oriente(90)
    while cy < y:
        av( min(1,y-cy) )
        cx,cy = position()

def suivre_chemin(traj):
    """
    traj est une liste de noeuds
    le robot se deplace direction Est/Sud/Sud-Est
    il rejoint le premier noeud de traj auquel il peut acceder
    """
    for x,y in p:
        cx,cy = position()
        if cx <= x and cy <= y:
            aller(x,y)


if __name__ == '__main__':
    init('robot_obstacles_invisibles')
    g = init_graph(xstart,xstop,gap)
    time.sleep(1)
    draw_graph(g)
    time.sleep(1)
    prune_nodes(g)
    draw_graph(g)
    time.sleep(1)

    p = nx.shortest_path(g,(xstart,xstart),(xstop,xstop),weight='weight')
    suivre_chemin(p)
