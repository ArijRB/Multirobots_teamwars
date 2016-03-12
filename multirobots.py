from robosim import *
from random import random,choice
import time

init('vide')
game.fps = 40
# Make 30 agents
def test():
    for i in range(80):
            p = game.add_players( (100+random()*250 , 100+random()*250) , game.player , tiled=False)
            if p:
                tournegauche( random()*360 ,p)

    time.sleep(2.5)
    joueurs = list(game.layers['joueur'])
    for i in range(200000):
        for p in game.layers['joueur']:
            p = choice(joueurs)
            tournegauche( random()*22-11, p)
            avance(1,p)
            game.mask.add_or_update_sprite(p)
            #time.sleep(0.001)
            break


test()
