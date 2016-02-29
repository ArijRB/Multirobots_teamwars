from robosim import *
from random import random


init('vide')
# Make 30 agents
for i in range(200):
    while True:
        p = game.add_player( random()*500 , random()*500 , game.player , tiled=False,draw_now=False)
        if p:
            p.rotate( random()*360 )
            break

for i in range(1000):
    for p in game.layers['joueur']:
        p.rotate( random()*3 )
        p.forward(1)
    game.mainiteration()
