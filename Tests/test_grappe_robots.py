from robosim import *
from random import random,choice
import time

init('vide')
game.auto_refresh = False

# Make 30 agents
def test():
    for i in range(80):
            p = game.add_players( (100+random()*250 , 100+random()*250) , game.player , tiled=False)
            if p:
                tournegauche( random()*360 ,p)

    joueurs = list(game.layers['joueur'])

    for i in range(500):
        for p in joueurs:
            tournegauche( random()*22-11,p)
            avance(2,p)
            #game.mask.add_or_update_sprite(p)
            #time.sleep(0.001)
        game.mainiteration()

if __name__ == '__main__':
    test()
