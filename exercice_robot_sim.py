from robot_sim import *
import numpy as np

while True:
    angles    = np.random.randint(360, size=10)
    distances = []

    for a in angles:
        setheading(a)
        distances.append( telemetre() )

    best = np.argmax(distances)
    setheading(angles[best])

    for t in range(int( distances[best]*0.8 )):
        avance(1)
