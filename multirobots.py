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
            #game.mask.add_or_update_sprite(p)
            #time.sleep(0.001)
            break


def test2():
    p1 = game.player
    set_position(50,100,p1)
    p2 = game.add_players( (100,100) , p1 , tiled=False)
    set_position(100,100,p2)
    oriente(0,p1)
    oriente(180,p2)
    for i in range(200000):
        avance(1,p1)
        avance(1,p2)
        time.sleep(0.1)
test2()
