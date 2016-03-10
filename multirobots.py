from robosim import *
from random import random


init('vide')
# Make 30 agents
for i in range(30):
        p = game.add_players( (100+random()*150 , 100+random()*150) , game.player , tiled=False,draw_now=True)
        if p:
            p.rotate( random()*360 )


for i in range(1000):
    for p in game.layers['joueur']:
        p.rotate( random()*6 )
        p.forward(1)
    game.mainiteration()