from gardenworld import *
from time import sleep

init()
p1 = game.player
p2 = game.add_players( (2,3) , game.player )
p3 = game.add_players( (3,4) , game.player )

for i in range(3):
    av(p1)
    sleep(1)
    av(p2)
    sleep(1)
    av(p3)
    sleep(1)
