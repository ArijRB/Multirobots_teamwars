#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirobot_teamwars.py
# Contact (ce fichier uniquement): nicolas.bredeche(at)upmc.fr
# Ce code utilise pySpriteWorld, développé par Yann Chevaleyre (U. Paris 13)
#
# Historique:
#   2016-03-28__23:23 - template pour 3i025 (IA&RO, UPMC, licence info)
#   2018-03-26__23:06 - mise à jour de l'énoncé du projet
#   2018-03-27__20:51 - reecriture de la fonction step(.)
# 	2018-03-28__10:00 - renommage de la fonction step(.) en stepController(.), refactoring
#
# Description:
#   Template pour projet multi-robots "MULTIROBOT WARS"
#
#       But du jeu: posséder le maximum de cases!
#           Chaque joueur dispose de quatre robots
#           Le monde est divisé en 1024 cases (ie. 32x32 cases de 16x16 pixels)
#           Le jeu tourne pendant 4000 itérations
#           Une case "appartient" à la dernière équipe qui l'a visitée
#
#       Ce que vous avez le droit de faire:
#           Seules modifications autorisées:
#               la méthode stepController(.) de la classe AgentTypeA
#               la valeur de la variable teamname de la classe AgentTypeA
#               [!] tout autre modification est exclue!
#           Les vitesses de translation et rotation et les distances renvoyées par les senseurs sont normalisées
#               translation/rotation: entre -1 et +1
#               distance à l'obstacle: entre 0 et +1
#               En pratique, les valeurs réelles maximales sont fixées par maxTranslationSpeed et maxRotationSpeed et  maxSensorDistance.
#           Liste *exhaustive* des informations que vous pouvez utiliser (cf. fonction stepController(.)):
#               sur soi-même:
#                   son propre numéro [non modifiable]
#                   sa propre position (x,y) [non modifiable]
#                   sa propre orientation [non modifiable]
#                   son état [modifiable, type: entier -- exclusivement!]
#               sur les éléments détectés par les senseurs:
#                   distance à l'obstacle
#                   type d'obstacle (rien, mur, robot)
#                       si robot:
#                           son identifiant
#                           son orientation
#                           sa position (x,y)
#
#       Contrainte imposée:
#           Votre comportement doit être *réactif*.
#           C'est à dire pas de mémoire (pas de variable globale, pas de carte, etc.)
#           ...A la seule et unique exception donnée par la possibilité d'utiliser la variable entière "etat". (exemple d'utilisation: mémoriser l'occurence d'un évènement particulier, mémoriser le comportement utilisé à t-1, etc.)
#
#       Remarques:
#           La méthode stepController() de multirobots.py illustre les senseurs autorisés
#           Lors de l'évaluation, les numéros de vos robots peuvent être différents.
#           Vous pouvez utiliser teamname pour reconnaitre les robots appartenant à la votre équipe (ou à l'équipe adverse)
#           [!!!] les commandes de translation/rotation sont exécutées *après* la fonction stepController(.). Par conséquent, seules les valeurs passées lors du dernier appel des fonctions setTranslationValue(.) et setRotationValue(.) sont prises en compte!
#
#       Recommandations:
#           Conservez intact multirobot_teamwars.py (travaillez sur une copie!)
#           Pour faire vos tests, vous pouvez aussi modifier (si vous le souhaitez) la méthode stepController() pour la classe AgentTypeB. Il ne sera pas possible de transmettre cette partie là lors de l'évaluation par contre.
#           La manière dont vous construirez votre fonction stepController(.) est libre. Par exemple: code écrit à la main, code obtenu par un processus d'apprentissage ou d'optimisation préalable, etc.; comportements individuels, collectifs, parasites (p.ex: bloquer l'adversaire), etc.
#
#       Evaluation:
#           Soutenance devant machine (par binome, 15 min.) lors de la dernière séance de TP (matin et après-midi)
#               Vous devrez m'envoyer votre code et un PDF de 2 pages résumant vos choix d'implémentation. Sujet: "[3i025] binome1, binome2", la veille de la soutenance
#               Vous devrez montrer votre résultat sur plusieurs arènes inédites
#               Vous devrez mettre en évidence la réutilisation des concepts vus en cours
#               Vous devrez mettre en évidence les choix pragmatiques que vous avez du faire
#               Assurez vous que la simple copie de votre fonctions stepController(.) dans le fichier multirobots_teamwars.py suffit pour pouvoir le tester
#           Vous affronterez vos camarades
#               Au tableau: une matrice des combats a mettre a jour en fonction des victoires et défaites
#               Affrontement sur les trois arènes inédites
#               vous pouvez utiliser http://piratepad.net pour échanger votre fonction stepController(.))
#       Bon courage!
# 
# Dépendances:
#   Python 2.x
#   Matplotlib
#   Pygame
#
# Aide: code utile
#   - Partie "variables globales": en particulier pour définir le nombre d'agents et l'arène utilisée. La liste SensorBelt donne aussi les orientations des différentes capteurs de proximité.
#   - La méthode "step" de la classe Agent, la variable teamname.
#   - La fonction setupAgents (permet de placer les robots au début de la simulation) - ne pas modifier pour l'évaluation
#   - La fonction setupArena (permet de placer des obstacles au début de la simulation) - ne pas modifier pour l'évaluation. Cependant, cela peut-être très utile de faire des arènes originales.
#

from robosim import *
from random import random, shuffle, randint
import time
import sys
import atexit
import math
import numpy as np

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  variables globales   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

game = Game()
agents = []

arena = 0

nbAgents = 8 # doit être pair et inférieur a 32
maxSensorDistance = 30              # utilisé localement.
maxRotationSpeed = 5
maxTranslationSpeed = 1
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  # angles en degres des senseurs

screen_width=512 #512,768,... -- multiples de 32  
screen_height=512 #512,768,... -- multiples de 32

maxIterations = 6000 # infinite: -1
showSensors = False
frameskip = 4   # 0: no-skip. >1: skip n-1 frames
verbose = False # permet d'afficher le suivi des agents (informations dans la console)

occupancyGrid = []
for y in range(screen_height/16):
    l = []
    for x in range(screen_width/16):
        l.append("_")
    occupancyGrid.append(l)



'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Agent "A"            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

class AgentTypeA(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    agentType = "A"
    
    
    translationValue = 0 # ne pas modifier directement
    rotationValue = 0 # ne pas modifier directement


    def __init__(self,robot):
        self.id = AgentTypeA.agentIdCounter
        AgentTypeA.agentIdCounter = AgentTypeA.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.robot.teamname = self.teamname
        self.etat = 0

    def getType(self):
        return self.agentType

    def getRobot(self):
        return self.robot

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR A -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-= pour l'évaluation, seul le teamname et la fct  stepController(.)  =-=
    # =-=-=-=-= seront utilisés. Assurez-vous donc que tout votre code utile est  =-=
    # =-=-=-=-= auto-contenu dans la fonction stepControlelr. Vous pouvez changer =-=
    # =-=-=-=-= teamname (c'est même conseillé si vous souhaitez que vos robots   =-=
    # =-=-=-=-= se reconnaissent entre eux.                                       =-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Titans" # A modifier avec le nom de votre équipe

    def stepController(self):
    
    	# cette méthode illustre l'ensemble des fonctions et informations que vous avez le droit d'utiliser.
    	# tout votre code doit tenir dans cette méthode. La seule mémoire autorisée est la variable self.etat
    	# (c'est un entier).
        sensorMinus80 = self.getDistanceAtSensor(1)
        sensorMinus40 = self.getDistanceAtSensor(2)
        sensorMinus20 = self.getDistanceAtSensor(3)
        sensorPlus20 = self.getDistanceAtSensor(4)
        sensorPlus40 = self.getDistanceAtSensor(5)
        sensorPlus80 = self.getDistanceAtSensor(6)
       

        params_avoid=[1.5,0.2,0.3,0.4,0.5,0.7,0.1,7.991821, -0.6982, -0.02061408,1,0.7639411, 7.9982821, -0.3943547820576982]
        params_suiv=[0.772411, 5.991, -0.39982, -0.24, 7.413656, -3.3062686, -5.7096, 8.516, -7.061587133381, -10.01849019654961, 3.64602, -6.2003122, -8.701892822852477, -6.060942]
        params_myTeam=[1.5,0.2,0.3,0.4,0.5,0.7,0.1,7.991821, -0.6982, -0.02061408,1,0.7639411, 7.9982821, -0.3943547820576982]
        params_explo=[1.5,0.2,0.3,0.4,0.5,0.7,0.1,7.441821, -0.820576982, -0.020604,1,0.7, 7.9941821, -0.3943547820576982]
        #Pour implementer l'ordre dans les architctures de  subsomption
        adversaire_bol=False
        my_team_bol=False
        mur_bol = False
        
        color( (0,255,0) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond vert autour de ce robot
        st=np.ones(8)
        s=np.ones(8)
        for i in range(len(SensorBelt)):
                if self.getObjectTypeAtSensor(i) == 2:
                    if self.getRobotInfoAtSensor(i)["teamname"]!= self.teamname  and (self.id % 4 == 0 or self.id % 4 == 1):
                       adversaire_bol=True
                       self.etat=-1
                       s[i]=self.getDistanceAtSensor(i)
                    else:
                       my_team_bol=True
                       team=i
                       st[i]=self.getDistanceAtSensor(i)
                elif self.getObjectTypeAtSensor(i) == 1:
                     mur_bol = True
        rotation=1
        translation=1
        if (self.id % 4 == 0 or self.id % 4 == 1):
                if (my_team_bol== True) and (team % 4 == 0 or team % 4 == 1):
                    sg = ( st[1]*1.5 + st[2]*1.5+st[3]+st[0]) / 5
                    sd = ( st[5] + st[6]*1.5+st[4]*1.5+st[7]) / 5
                    rotation=sd-sg
                    translation=1
                    
                elif(adversaire_bol == True):
                    sg = ( s[1]*1.5 + s[2]*1.5+s[3]+s[0]) / 5
                    sd = ( s[5] + s[6]*1.5+s[4]*1.5+s[7]) / 5
                    rotation=sg-sd
                    translation=1 
                elif (my_team_bol== True) :
                    sg = ( st[1]*1.5 + st[2]*1.5+st[3]+st[0]) / 5
                    sd = ( st[5] + st[6]*1.5+st[4]*1.5+st[7]) / 5
                    rotation=sd-sg
                    translation=1
                elif (mur_bol == True):
                     translation =  math.tanh( sensorMinus40 * params_avoid[0] + sensorMinus20 * params_avoid[1] + sensorPlus20 * params_avoid[2] + sensorPlus40 * params_avoid[3] + params_avoid[4] ) 
                     rotation =  math.tanh( sensorMinus40 * params_avoid[5] + sensorMinus20 * params_avoid[6] + sensorPlus20 * params_avoid[7] + sensorPlus40 * params_avoid[8] + params_avoid[9] )

        else:
            if (mur_bol == True):
                sg = ( self.getDistanceAtSensor(1)*1.5 + self.getDistanceAtSensor(2)*1.5+self.getDistanceAtSensor(3)+self.getDistanceAtSensor(0)) / 5
                sd = ( self.getDistanceAtSensor(5) + self.getDistanceAtSensor(6)*1.5+self.getDistanceAtSensor(4)*1.5+self.getDistanceAtSensor(7)) / 5
                rotation=sd-sg
                translation=1
            else:
                sg = ( self.getDistanceAtSensor(1)*1.5 + self.getDistanceAtSensor(2)*1.5+self.getDistanceAtSensor(3)+self.getDistanceAtSensor(0)) / 5
                sd = ( self.getDistanceAtSensor(5) + self.getDistanceAtSensor(6)*1.5+self.getDistanceAtSensor(4)*1.5+self.getDistanceAtSensor(7)) / 5
                rotation=sd-sg
                translation=1
        if (iteration !=0 and self.etat != -1):
            x=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
            if (self.etat==x):
                rotation=-0.2
                translation=1
            self.etat=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
        elif iteration ==0:
            self.etat=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
        self.setRotationValue(rotation)
        self.setTranslationValue(translation)


        return

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def step(self):
        self.stepController()
        self.move()

    def move(self):
        self.robot.forward(self.translationValue)
        self.robot.rotate(self.rotationValue)

    def getDistanceAtSensor(self,id):
        sensor_infos = sensors[self.robot] # sensor_infos est une liste de namedtuple (un par capteur).
        return min(sensor_infos[id].dist_from_border,maxSensorDistance) / maxSensorDistance

    def getObjectTypeAtSensor(self,id):
        if sensors[self.robot][id].dist_from_border > maxSensorDistance:
            return 0 # nothing
        elif sensors[self.robot][id].layer == 'joueur':
            return 2 # robot
        else:
            return 1 # wall/border

    def getRobotInfoAtSensor(self,id):
        if sensors[self.robot][id].dist_from_border < maxSensorDistance and sensors[self.robot][id].layer == 'joueur':
            otherRobot = sensors[self.robot][id].sprite
            info = {'id': otherRobot.numero, 'centroid': otherRobot.get_centroid(), 'orientation': otherRobot.orientation(), 'teamname': otherRobot.teamname }
            return info
        else:
            #print "[WARNING] getPlayerInfoAtSensor(.): not a robot!"
            return None

    def setTranslationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxTranslationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxTranslationSpeed
        else:
            value = value * maxTranslationSpeed
        self.translationValue = value

    def setRotationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxRotationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxRotationSpeed
        else:
            value = value * maxRotationSpeed
        self.rotationValue = value


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Agent "B"            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

class AgentTypeB(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    agentType = "B"
    etat = 0
    
    translationValue = 0
    rotationValue = 0

    def __init__(self,robot):
        self.id = AgentTypeB.agentIdCounter
        AgentTypeB.agentIdCounter = AgentTypeB.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.robot.teamname = self.teamname


    def getType(self):
        return self.agentType

    def getRobot(self):
        return self.robot


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR B -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Equipe Test" # A modifier avec le nom de votre équipe

    def stepController(self):

        color( (0,0,255) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot

        distGauche = self.getDistanceAtSensor(2) # renvoi une valeur normalisée entre 0 et 1
        distDroite = self.getDistanceAtSensor(5) # renvoi une valeur normalisée entre 0 et 1
        
        if distGauche < distDroite:
            self.setRotationValue( +1 )
        elif distGauche > distDroite:
            self.setRotationValue( -1 )
        else:
            self.setRotationValue( 0 )

        self.setTranslationValue(1) # normalisé -1,+1
#        sg = ( self.getDistanceAtSensor(1)*1.5 + self.getDistanceAtSensor(2)*1.5+self.getDistanceAtSensor(3)+self.getDistanceAtSensor(0)) / 5
#        sd = ( self.getDistanceAtSensor(5) + self.getDistanceAtSensor(6)*1.5+self.getDistanceAtSensor(4)*1.5+self.getDistanceAtSensor(7)) / 5
#                
#        self.setRotationValue(sd-sg)
#        self.setTranslationValue(1)
#        
		# monitoring (optionnel - changer la valeur de verbose)
        if verbose == True:
	        print "Robot #"+str(self.id)+" [teamname:\""+str(self.teamname)+"\"] [variable mémoire = "+str(self.etat)+"] :"
	        for i in range(8):
	            print "\tSenseur #"+str(i)+" (angle: "+ str(SensorBelt[i])+"°)"
	            print "\t\tDistance  :",self.getDistanceAtSensor(i)
	            print "\t\tType      :",self.getObjectTypeAtSensor(i) # 0: nothing, 1: wall/border, 2: robot
	            print "\t\tRobot info:",self.getRobotInfoAtSensor(i) # dict("id","centroid(x,y)","orientation") (if not a robot: returns None and display a warning)

        return

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def step(self):
        self.stepController()
        self.move()

    def move(self):
        self.robot.forward(self.translationValue)
        self.robot.rotate(self.rotationValue)

    def getDistanceAtSensor(self,id):
        sensor_infos = sensors[self.robot] # sensor_infos est une liste de namedtuple (un par capteur).
        return min(sensor_infos[id].dist_from_border,maxSensorDistance) / maxSensorDistance

    def getObjectTypeAtSensor(self,id):
        if sensors[self.robot][id].dist_from_border > maxSensorDistance:
            return 0 # nothing
        elif sensors[self.robot][id].layer == 'joueur':
            return 2 # robot
        else:
            return 1 # wall/border

    def getRobotInfoAtSensor(self,id):
        if sensors[self.robot][id].dist_from_border < maxSensorDistance and sensors[self.robot][id].layer == 'joueur':
            otherRobot = sensors[self.robot][id].sprite
            info = {'id': otherRobot.numero, 'centroid': otherRobot.get_centroid(), 'orientation': otherRobot.orientation(), 'teamname': otherRobot.teamname }
            return info
        else:
            #print "[WARNING] getPlayerInfoAtSensor(.): not a robot!"
            return None


    def setTranslationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxTranslationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxTranslationSpeed
        else:
            value = value * maxTranslationSpeed
        self.translationValue = value

    def setRotationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxRotationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxRotationSpeed
        else:
            value = value * maxRotationSpeed
        self.rotationValue = value


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions init/step  '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''


def setupAgents():
    global screen_width, screen_height, nbAgents, agents, game

    # Make agents

    nbAgentsTypeA = nbAgentsTypeB = nbAgents / 2
    nbAgentsCreated = 0

    for i in range(nbAgentsTypeA):
        p = game.add_players( (16 , 200+32*i) , None , tiled=False)
        p.oriente( 0 )
        p.numero = nbAgentsCreated
        nbAgentsCreated = nbAgentsCreated + 1
        agents.append(AgentTypeA(p))

    for i in range(nbAgentsTypeB):
        p = game.add_players( (486 , 200+32*i) , None , tiled=False)
        p.oriente( 180 )
        p.numero = nbAgentsCreated
        nbAgentsCreated = nbAgentsCreated + 1
        agents.append(AgentTypeB(p))

    game.mainiteration()



def setupArena0():
    for i in range(6,13):
        addObstacle(row=3,col=i)
    for i in range(3,10):
        addObstacle(row=12,col=i)
    addObstacle(row=4,col=12)
    addObstacle(row=5,col=12)
    addObstacle(row=6,col=12)
    addObstacle(row=11,col=3)
    addObstacle(row=10,col=3)
    addObstacle(row=9,col=3)

def setupArena1():
    return

def setupArena2():
    for i in range(0,8):
        addObstacle(row=i,col=7)
    for i in range(8,16):
        addObstacle(row=i,col=8)

def updateSensors():
    global sensors 
    # throw_rays...(...) : appel couteux (une fois par itération du simulateur). permet de mettre à jour le masque de collision pour tous les robots.
    sensors = throw_rays_for_many_players(game,game.layers['joueur'],SensorBelt,max_radius = maxSensorDistance+game.player.diametre_robot() , show_rays=showSensors)

def stepWorld():
    efface()
    
    updateSensors()

    # chaque agent se met à jour. L'ordre de mise à jour change à chaque fois (permet d'éviter des effets d'ordre).
    shuffledIndexes = [i for i in range(len(agents))]
    shuffle(shuffledIndexes)
    for i in range(len(agents)):
        agents[shuffledIndexes[i]].step()
        # met à jour la grille d'occupation
        coord = agents[shuffledIndexes[i]].getRobot().get_centroid()
        occupancyGrid[int(coord[0])/16][int(coord[1])/16] = agents[shuffledIndexes[i]].getType() # first come, first served
    return


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions internes   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

def addObstacle(row,col):
    # le sprite situe colone 13, ligne 0 sur le spritesheet
    game.add_new_sprite('obstacle',tileid=(0,13),xy=(col,row),tiled=True)

class MyTurtle(Turtle): # also: limit robot speed through this derived class
    maxRotationSpeed = maxRotationSpeed # 10, 10000, etc.
    def rotate(self,a):
        mx = MyTurtle.maxRotationSpeed
        Turtle.rotate(self, max(-mx,min(a,mx)))

def displayOccupancyGrid():
    global iteration
    nbA = nbB = nothing = 0

    for y in range(screen_height/16):
        for x in range(screen_width/16):
            sys.stdout.write(occupancyGrid[x][y])
            if occupancyGrid[x][y] == "A":
                nbA = nbA+1
            elif occupancyGrid[x][y] == "B":
                nbB = nbB+1
            else:
                nothing = nothing + 1
        sys.stdout.write('\n')

    sys.stdout.write('Time left: '+str(maxIterations-iteration)+'\n')
    sys.stdout.write('Summary: \n')
    sys.stdout.write('\tType A: ')
    sys.stdout.write(str(nbA))
    sys.stdout.write('\n')
    sys.stdout.write('\tType B: ')
    sys.stdout.write(str(nbB))
    sys.stdout.write('\n')
    sys.stdout.write('\tFree  : ')
    sys.stdout.write(str(nothing))
    sys.stdout.write('\n')
    sys.stdout.flush() 

    return nbA,nbB,nothing

def onExit():
    ret = displayOccupancyGrid()
    print "\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
    if ret[0] > ret[1]:
        print "Robots type A (\"" + str(AgentTypeA.teamname) + "\") wins!"
    elif ret[0] < ret[1]:
        print "Robots type B (\"" + str(AgentTypeB.teamname) + "\") wins!"
    else: 
        print "Nobody wins!"
    print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
    print "\n[Simulation::stop]"


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Main loop            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

init('empty',MyTurtle,screen_width,screen_height) # display is re-dimensioned, turtle acts as a template to create new players/robots
game.auto_refresh = False # display will be updated only if game.mainiteration() is called
game.frameskip = frameskip
atexit.register(onExit)

if arena == 0:
    setupArena0()
elif arena == 1:
    setupArena1()
else:
    setupArena2()

setupAgents()
game.mainiteration()

iteration = 0
while iteration != maxIterations:
    stepWorld()
    game.mainiteration()
    if iteration % 200 == 0:
        displayOccupancyGrid()
    iteration = iteration + 1

