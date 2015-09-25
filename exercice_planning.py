from robosim import *
import networkx as nx
from math import sqrt
def first(gen): return list(gen)[0]
def last(gen):  return list(gen)[-1]

init()
gap = 30
coord_gen = range(80,470,gap)
fst,lst= first(coord_gen),last(coord_gen)

def init_graph():
    g = nx.Graph()

    for i in coord_gen:
        for j in coord_gen:
            if i > fst and j < lst:
                g.add_edge( (i,j),(i-gap,j+gap),weight=1.0)
            if j < lst:
                g.add_edge( (i,j),(i,j+gap),weight=1.0)
            if i < lst:
                g.add_edge( (i,j),(i+gap,j),weight=1.0)
            if j < lst and i < lst:
                g.add_edge( (i,j),(i+gap,j+gap),weight=1.414)
    return g

def draw_graph(g):
    efface()
    for (i1,j1),(i2,j2) in g.edges():
        line(i1,j1,i2,j2,wait=True)
    line(fst,fst,fst,fst,wait=False)

def prune_nodes(g):
    for i in coord_gen:
        for j in coord_gen:
            if obstacle_coords(i,j):
                g.remove_node( (i,j) )
    draw_graph(g)
    raw_input()
    for (i1,j1),(i2,j2) in g.edges():
        if  i1 != i2 and j1 != j2 and not g.has_edge( (i1,j2),(i2,j1) ):
            g.remove_edge( (i1,j1),(i2,j2) )

def vaa(x,y):
    cx,cy = position()
    oriente(45)
    while x > cx and y > cy:
        av(1)
        cx,cy = position()
    oriente(0)
    while x > cx:
        av(1)
        cx,cy = position()
    oriente(90)
    while y > cy:
        av(1)
        cx,cy = position()
    return True

g = init_graph()
draw_graph(g)
raw_input()
prune_nodes(g)
draw_graph(g)
p = nx.shortest_path(g,(fst,fst),(lst,lst),weight='weight')

teleporte(80,80)
for x,y in p[1:]:
    vaa(x,y)
