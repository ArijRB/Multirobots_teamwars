from robosim import *
import numpy as np

init()

while True:
    angles = np.random.randint(360, size=1)
    distances = []

    for a in angles:
        oriente(a)
        distances.append(telemetre())

    best = np.argmax(distances)
    oriente(angles[best])

    while not obstacle():
        avance(1)
