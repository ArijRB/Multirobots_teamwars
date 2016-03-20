# Pour lancer ces tests, taper python -m 'Tests.*'

from robosim import *
import numpy as np
import time


def main():
    Turtle.set_turtle_size(18)

    init()
    #game.frameskip = 5

    for i in range(20):
        angles = np.random.randint(360, size=1)
        distances = []

        for a in angles:
            oriente(a)
            if i % 2:
                distances.append(telemetre()) # testing function telemetre
            else:
                cx,cy = game.player.get_centroid()
                distances.append( telemetre_coords(cx,cy,a) ) # testing function telemetre_coords

        best = np.argmax(distances)
        oriente(angles[best])

        while not obstacle(2):
            avance(2)
            #time.sleep(0.1)
    Turtle.set_turtle_size(22)

if __name__ == '__main__':
    main()
