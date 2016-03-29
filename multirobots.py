#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirobot.py
# Contact (ce fichier uniquement): nicolas.bredeche(at)upmc.fr
# 
# Description:
#   Template pour simulation mono- et multi-robots type khepera/e-puck/thymio
#   Ce code utilise pySpriteWorld, développé par Yann Chevaleyre (U. Paris 13)
# 
# Dépendances:
#   Python 2.x
#   Matplotlib
#   Pygame
# 
# Historique: 
#   2016-03-28__23:23 - template pour 3i025 (IA&RO, UPMC, licence info)
#
# Aide: code utile
#   - Partie "variables globales"
#   - La méthode "step" de la classe Agent
#   - La fonction setupAgents (permet de placer les robots au début de la simulation)
#   - La fonction setupArena (permet de placer des obstacles au début de la simulation)
#   - il n'est pas conseillé de modifier les autres parties du code.
# 

from robosim import *
from random import random, shuffle
import time
import sys

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Aide                 '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

#game.setMaxTranslationSpeed(3) # entre -3 et 3
# size of arena: 
#   screenw,screenh = taille_terrain()
#   OU: screen_width,screen_height

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  variables globales   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

game = Game()

agents = []
screen_width=512 #512,768,... -- multiples de 32  
screen_height=512 #512,768,... -- multiples de 32
nbAgents = 10

maxSensorDistance = 30              # utilisé localement.
maxRotationSpeed = 5
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  # angles en degres des senseurs

maxIterations = -1 # infinite: -1

showSensors = True
frameskip = 0   # 0: no-skip. >1: skip n-1 frames
verbose = True

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Classe Agent/Robot   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

class Agent(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1

    def __init__(self,robot):
        self.id = Agent.agentIdCounter
        Agent.agentIdCounter = Agent.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot

    def step(self):

        #print "robot #", self.id, " -- step"

        p = self.robot

        # actions
        p.rotate( random()*maxRotationSpeed )   # normalisé -1,+1 -- valeur effective calculé avec maxRotationSpeed et maxTranslationSpeed
        p.forward(1) # normalisé -1,+1

        #Exemple: comment récuperer le senseur #2
        #dist = sensor_infos[2].dist_from_border
        #if dist > maxSensorDistance:
        #    dist = maxSensorDistance # borne

        # monitoring - affiche diverses informations sur l'agent et ce qu'il voit.
        # pour ne pas surcharger l'affichage, je ne fais ca que pour le player 1
        if verbose == True and self.id == 0:

            efface()    # j'efface le cercle bleu de l'image d'avant
            color( (0,0,255) )
            circle( *game.player.get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot

            print "\n# Current robot at " + str(p.get_centroid()) + " with orientation " + str(p.orientation())

            sensor_infos = sensors[p] # sensor_infos est une liste de namedtuple (un par capteur).
            for i,impact in enumerate(sensors[p]):  # impact est donc un namedtuple avec plein d'infos sur l'impact: namedtuple('RayImpactTuple', ['sprite','layer','x', 'y','dist_from_border','dist_from_center','rel_angle_degree','abs_angle_degree'])
                if impact.dist_from_border > maxSensorDistance:
                    print "- sensor #" + str(i) + " touches nothing"
                else:
                    print "- sensor #" + str(i) + " touches something at distance " + str(impact.dist_from_border)
                    if impact.layer == 'joueur':
                        playerTMP = impact.sprite
                        print "  - type: robot"
                        print "    - x,y = " + str( playerTMP.get_centroid() ) + ")" # renvoi un tuple
                        print "    - orientation = " + str( playerTMP.orientation() ) + ")" # p/r au "nord"
                    elif impact.layer == 'obstacle':
                        print "  - type obstacle"
                    else:
                        print "  - type boundary of window"
        return


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions init/step  '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''


def setupAgents():
    global screen_width, screen_height, nbAgents, agents, game

    # Make agents
    for i in range(nbAgents):
        while True:
            p = -1
            while p == -1: # p renvoi -1 s'il n'est pas possible de placer le robot ici (obstacle)
                p = game.add_players( (random()*screen_width , random()*screen_height) , None , tiled=False)
            if p:
                p.oriente( random()*360 )
                agents.append(Agent(p))
                break
    game.mainiteration()


def setupArena():
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



def stepWorld():
    # chaque agent se met à jour. L'ordre de mise à jour change à chaque fois (permet d'éviter des effets d'ordre).
    shuffledIndexes = [i for i in range(len(agents))]
    shuffle(shuffledIndexes)     ### TODO: erreur sur macosx
    for i in range(len(agents)):
        agents[shuffledIndexes[i]].step()
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


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Main loop            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

init('vide3',MyTurtle,screen_width,screen_height) # display is re-dimensioned, turtle acts as a template to create new players/robots
game.auto_refresh = False # display will be updated only if game.mainiteration() is called
game.frameskip = frameskip

setupArena()
setupAgents()
game.mainiteration()

i = 0
while i != maxIterations:
    # c'est plus rapide d'appeler cette fonction une fois pour toute car elle doit recalculer le masque de collision,
    # ce qui est lourd....
    sensors = throw_rays_for_many_players(game,game.layers['joueur'],SensorBelt,max_radius = maxSensorDistance+game.player.diametre_robot() , show_rays=showSensors)
    stepWorld()
    game.mainiteration()
