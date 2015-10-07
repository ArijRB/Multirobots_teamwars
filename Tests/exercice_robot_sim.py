# Pour lancer ces tests, taper python -m 'Tests.*'

from robosim import *
import numpy as np



def main():
    rs.fps = 100
    init()

    for i in range(20):
        angles = np.random.randint(360, size=1)
        distances = []

        for a in angles:
            oriente(a)
            distances.append(telemetre())

        best = np.argmax(distances)
        oriente(angles[best])

        while not obstacle(4):
            avance(4)

if __name__ == '__main__':
    main()
