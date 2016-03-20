from robosim import *
from random import random


init('vide')

# Arene

game.addObstacle(100,100,40,30) # x,y,width,height -- pas la peine de prévoir un remove
game.addObstacle(200,200,40,30,255,255,255) # idem, avec couleur RGB (valeurs: 0...255)
print "Arene: " + str(game.getArenaDimensions) # donne width height de l'arene

# Initialisation robots

maxSensorDistance = 16 # utilisé localement.
setSensorBelt(8,maxSensorDistance) # (nb of sensors, length) -- la repartition des senseurs est homogène autour du robot. Si nombre impair, alors le premier senseur pointe vers l'avant, sinon (nb paire) le premier est le dernier senseur sont décalés de +x° et -x° p/r à l'avant.

# ce qui suit est pour permettre de mettre toutes les valeurs entre -1 et 1. Puis de renormaliser automatiquement
game.setMaxRotationSpeed(10) # donc entre -10 et 10
game.setMaxTranslationSpeed(3) # donc entre -3 et 3

# Make 30 agents
for i in range(20):
    while True:
        p = -1
        while p == -1: # p renvoi -1 s'il n'est pas possible de placer le robot ici (obstacle)
	        p = game.add_players( (random()*500 , random()*500) , game.player , tiled=False,draw_now=True)
        if p:
            p.rotate( random()*360 )
            break

# Rendu
displaySensors(True)

for i in range(1000):
    for p in game.layers['joueur']:
    	print "# Current robot at " + str(p.getCoord()) + " with orientation " + str(p.getOrientation())

        p.rotate( random()*3 )   # normalisé -1,+1 -- valeur effective calculé avec maxRotationSpeed et maxTranslationSpeed
        p.forward(1) # normalisé -1,+1
        sensors = p.getSensorInformation() # tableau de tuples, chaque tuple: (distance, type)
        for i in range(len(sensors)):
        	if sensors[i][0] = maxSensorDistance:
        		print "- sensor #" + str(i) + " touches nothing"
        	else:
        		print "- sensor #" + str(i) + " touches something at distance " + str(sensors[i][0])
        		print "  - touches object of type #" + str(sensors[i][1])
        		if str(sensors[i][1]) == 1:
        			print "  - type: obstacle"
        		elif str(sensors[i][1]) == 2:
        			playerTMP = getRobotTouchedBySensor[i]
        			print "  - type: robot"
        			print "    - x,y = " + playerTMP.getCoord() + ")" # renvoi un tuple
        			print "    - orientation = " + playerTMP.getOrientation() + ")" # p/r au "nord"
        		else
        			print "  - unknown type"

    game.mainiteration()
