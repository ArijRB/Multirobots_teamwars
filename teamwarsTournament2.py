#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirobot_teamwars.py
# Contact (ce fichier uniquement): nicolas.bredeche(at)upmc.fr
# Ce code utilise pySpriteWorld, développé par Yann Chevaleyre (U. Paris 13)
#
# Historique:
# 	2018-04-09__16:35 - version pour examen 2018
#
# Dépendances:
#   Python 2.x
#   Matplotlib
#   Pygame
#
# Description:
#   Template pour projet multi-robots "MULTIROBOT WARS"
#   Les équipes "verte" et "bleue" ont chacune une stratégie d'exploration
#
# Mode d'emploi pour l'évaluation:
#   Mettre votre fonction stepController() à la place de celle de AgentTypeA
#   Tout autre modification est interdite
#   Vous êtes l'équipe verte
#   Pour lancer le code: "python teamwarsTournament.py <numero_de_l'arene>" avec <numero_de_l'arene> = 0, 1, 2, 3 ou 4
#
# Mode d'emploi pour un tournoi entre deux équipes:
#   Une équipe copie sa fonction stepController dans AgentTypeA
#   L'autre équipe fait de même avec AgentTypeB
#   Evaluation sur 10 matchs:
#       1. testez avec chacune des 5 arènes (variable "arena" ci-dessous, valeurs de 0 à 4)
#       2. pour chaque arène, testez deux fois, en échangeant la position initiale entre chaque essais (variable "invertInitPop" ci-dessous)
#   Pour lancer le code: "python teamwarsTournament.py <numero_de_l'arene> <position_standard>"
#       avec <numero_de_l'arene> = 0, 1, 2, 3 ou 4
#       avec <position_standard> = True ou False (False (par défaut): l'équipe verte commence à gauche, sinon, l'inverse)
#   => Comptez le nombre de victoires de chacun. En cas d'égalité: +0.5 point chacun.
#
#

from robosim import *
from random import random, shuffle, randint,uniform
import time
import sys
import atexit
import math
import numpy as np
''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''
''' Paramètres du Tournoi  '''
''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''

# Quelle arêne? (valeurs de 0 à 4)
arena = 0

# Position de départ? (si la valeur est vraie, alors les deux équipes échangent leur position de départ)
invertInitPop = False

''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''
'''  variables globales    '''
''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''

game = Game()
agents = []

running = False

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
    etat = 0
    
    translationValue = 0 # ne pas modifier directement
    rotationValue = 0 # ne pas modifier directement


    def __init__(self,robot):
        self.id = AgentTypeA.agentIdCounter
        AgentTypeA.agentIdCounter = AgentTypeA.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.robot.teamname = self.teamname

    def getType(self):
        return self.agentType

    def getRobot(self):
        return self.robot

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR A -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Equipe VERTE" # A modifier avec le nom de votre équipe

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
          
        #Pour implementer l'ordre dans les architctures de  subsomption
        adversaire_bol=False
        my_team_bol=False
        mur_bol = False
        
        color( (0,255,0) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond vert autour de ce robot
        
        #Pour detecter les sensors activées qui indique la presence d'un autre joueur soit adversaire ou de notre equipe
        st=np.ones(8)
        s=np.ones(8)
        sm=np.ones(8)
        for i in range(len(SensorBelt)):
            if self.getObjectTypeAtSensor(i) == 2:
                if self.getRobotInfoAtSensor(i)["teamname"]!= self.teamname  and (self.id % 4 == 0 or self.id % 4 == 1):
                    adversaire_bol=True
                    self.etat=-1
                    s[i]=self.getDistanceAtSensor(i)
                else:
                    my_team_bol=True
                    team=(self.getRobotInfoAtSensor(i))["id"]
                    st[i]=self.getDistanceAtSensor(i)
            elif self.getObjectTypeAtSensor(i) == 1:
                    mur_bol = True
                    sm[i]=self.getDistanceAtSensor(i)
        #les comportements selon les robots
         
        if (self.id % 4 == 0 or self.id % 4 == 1):#agents gourmands
                if (my_team_bol== True) and (team % 4 == 0 or team % 4 == 1):
                    sg = ( st[1]*1.5 + st[2]*1.5+st[3]+st[0]) / 5
                    sd = ( st[5] + st[6]*1.5+st[4]*1.5+st[7]) / 5
                    rotation=sd-sg
                    translation=1
                    self.etat=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
                elif(adversaire_bol == True):
                    sg = ( s[1]*1.5 + s[2]*1.5+s[3]+s[0]) / 5
                    sd = ( s[5] + s[6]*1.5+s[4]*1.5+s[7]) / 5
                    rotation=sg-sd
                    translation=1 
                elif (my_team_bol== True) :
                    sg = ( st[1]*1.5 + st[2]*1.5+st[3]+st[0]+2) / 7
                    sd = ( st[5] + st[6]*1.5+st[4]*1.5+st[7]+2)/ 7
                    rotation=sd-sg
                    translation=1
                    self.etat=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
                elif (mur_bol == True):
                    sg = ( self.getDistanceAtSensor(1)*1.5 + self.getDistanceAtSensor(2)*1.5+self.getDistanceAtSensor(3)+self.getDistanceAtSensor(0)) / 5
                    sd = ( self.getDistanceAtSensor(5) + self.getDistanceAtSensor(6)*1.5+self.getDistanceAtSensor(4)*1.5+self.getDistanceAtSensor(7)) / 5
                    rotation=sd-sg
                    translation=1
                else:
                    rotation=uniform(-1,1)
                    translation=1

        else:#agents explorateurs
            if iteration ==0 and self.id % 4 == 2 :
                rotation=1
                translation=-1
            else:
                if (mur_bol == True):
                    sg = ( self.getDistanceAtSensor(1)*1.5 + self.getDistanceAtSensor(2)*1.5+self.getDistanceAtSensor(3)+self.getDistanceAtSensor(0)) / 5
                    sd = ( self.getDistanceAtSensor(5) + self.getDistanceAtSensor(6)*1.5+self.getDistanceAtSensor(4)*1.5+self.getDistanceAtSensor(7)) / 5
                    rotation=sd-sg
                    translation=1
                elif (my_team_bol== True) :
                    sg = ( st[1]*1.5 + st[2]*1.5+st[3]+st[0]+2) / 7
                    sd = ( st[5] + st[6]*1.5+st[4]*1.5+st[7]+2)/ 7
                    rotation=sd-sg
                    translation=1
                else:
                    rotation=uniform(-1,1)
                    translation=1
        if (iteration !=0 and self.etat != -1):
            x=self.getRobot().get_centroid()[0],self.getRobot().get_centroid()[1]
            if (self.etat==x):
                rotation=-0.1
                translation=0.95
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
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Phobos" # A modifier avec le nom de votre équipe

    def stepController(self):
        
        color( (0,0,255) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot

        class Comportement:
    
            def activable(self,agent):
                ''' Dis si ce comportement est activable dans la situation actuelle '''
                print("ERROR : ACTIVABLE PAS IMPLEMENTE")
                pass
                
            def action(self,agent):
                ''' Dis si ce que l'agent doit faire dans la situation actuelle '''
                print("ERROR : ACTIION PAS IMPLEMENTE")
                pass
        
        class AvoidWall(Comportement):
            ''' Classe statique qui permet d'éviter les murs et les robots '''
            
            name = "avoidWall"
            def activable(self,agent):
                ''' Toujours activable '''
                return True
            
            def action(self,agent):
                ''' Retourne la translation et la rotation du robot pour éviter les murs et les autres robots'''
                translation = 0
                rotation = 0
                
                sensorMinus40 = agent.getDistanceAtSensor(2)
                sensorMinus20 = agent.getDistanceAtSensor(3)
                sensorPlus20 = agent.getDistanceAtSensor(4)
                sensorPlus40 = agent.getDistanceAtSensor(5)
        
                params1 = [4.00078262582386, 10, 10, 10, 4.528076086234666, 3.0559303936812587, 3.4134803115361976, 10, 10, 0.6290254154562023]
                params = [-1 + (1 - math.cos((math.pi * i)/10)) for i in params1]
                if len(params) != 10: # vérifie que le nombre de paramètres donné est correct
                    print "[ERROR] number of parameters is incorrect. Exiting."
                    exit()
        
                translation=1
                rotation =  math.tanh( sensorMinus40 * params[5] + sensorMinus20 * params[6] + sensorPlus20 * params[7] + sensorPlus40 * params[8] + params[9] )
        
                #print "robot #", self.id, "[r =",rotation," - t =",translation,"]"
        
                return (translation,rotation)
                
        class Suiveur(Comportement):
            ''' Classe statique qui permet de suivre un robot adverse '''
            name = "suiveur"
            
            def activable(self,agent):
                ''' Activable si un robot adverse est proche de nous '''
                presence_allie=0
                presence_ennemi=0
                (posx_allie,posy_allie)=(0,0)
                (posx_ennemi, posy_ennemi)=(0,0)
                for i in range(1,7):
                    if agent.getDistanceAtSensor(i) < 1 and agent.getObjectTypeAtSensor(i) == 2:
                        if agent.getRobotInfoAtSensor(i)['teamname'] != 'Phobos':
                            presence_ennemi=1
                        else:
                            presence_allie=1
                            (posx_allie, posy_allie)=agent.getRobotInfoAtSensor(i)['centroid']
                if presence_allie==1 :
                    if(math.sqrt(pow(posy_ennemi-agent.getRobot().get_centroid()[1],2)+math.sqrt(pow(posx_ennemi-agent.getRobot().get_centroid()[0], 2)>math.sqrt(pow(posx_ennemi-posx_allie,2))+math.sqrt(pow(posy_ennemi-posy_allie, 2))))):
                        return False
                if presence_ennemi==1:
                    return True
                else:
                    return False
            
            def action(self,agent):
                ''' Retourne la translation et la rotation du robot pour suivre le robot adverse qu'il voit dans son viseur '''
                for i in range(1,7):
                    if agent.getDistanceAtSensor(i) < 1 and agent.getObjectTypeAtSensor(i) == 2:
                        if agent.getRobotInfoAtSensor(i)['teamname'] != 'Phobos':
                            trans = 1
                            rot = SensorBelt[i]/180
                            (posx_ennemi, posy_ennemi)=agent.getRobotInfoAtSensor(i)['centroid']
                return (trans,rot)
         
        class Bloqueur(Comportement):
            ''' Classe statique qui permet bloquer un robot qui nous suivent '''
            name = "bloqueur"
            
            def activable(self,agent):
                ''' Activable si un robot adverse est proche de nous '''
                if agent.getDistanceAtSensor(0) < 1 or agent.getDistanceAtSensor(7) < 1:
                    if agent.getObjectTypeAtSensor(0) == 2 or agent.getObjectTypeAtSensor(7) == 2:
                        if agent.getRobotInfoAtSensor(0) != None:
                            return True
                        elif agent.getRobotInfoAtSensor(7) != None:
                            return True
                
                return False
            
            def action(self,agent):
                ''' Retourne la translation et la rotation du robot pour suivre le robot adverse qu'il voit dans son viseur '''
                
                if agent.getDistanceAtSensor(0) < 1 or agent.getDistanceAtSensor(7) < 1:
                    if agent.getObjectTypeAtSensor(0) == 2 or agent.getObjectTypeAtSensor(7) == 2:
                        if agent.getRobotInfoAtSensor(0) != None:
                            return (1,1)
                        elif agent.getRobotInfoAtSensor(7) != None:
                            return (1,1)
            
        class Subsomption:
            ''' Définit une architecture de subsomption '''
            
            def __init__(self):
                self.listeComportements = {}
            
            def addComportement(self,comport,prio):
                self.listeComportements[comport.name] = (comport,prio)
                
            def checkValide(self,agent):
                resultat = []
                for c in self.listeComportements:
                    if self.listeComportements[c][0].activable(agent) == True:
                        resultat.append(c)
                return resultat
            
            def actionChoisie(self,agent):
                
                # On choicit l'action appropriée
                listePossibles = self.checkValide(agent)
                act = ([],-1)
                for i in listePossibles:
                    if self.listeComportements[i][1] > act[1]:
                        act = (i,self.listeComportements[i][1])
                
                #On l'effectue
                
                return self.listeComportements[act[0]][0].action(agent)
        
        maSub1 = Subsomption()
        maSub1.addComportement(AvoidWall(),0)
        maSub1.addComportement(Suiveur(),2)
        maSub1.addComportement(Bloqueur(),3)

        
        
        ####### FIN DES CLASSES #########
        
        
        x_state=int(self.etat%pow(2,20)/pow(2,10))
        y_state=int(self.etat%1024)
        m_state=int(self.etat/pow(2,20))
        continuous_state=int(self.etat/pow(2,22))
        if(continuous_state>0):
            continuous_state-=1
        elif(x_state==int(self.getRobot().get_centroid()[0]) and y_state==int(self.getRobot().get_centroid()[1]) and m_state==0):
            rotation=0
            translation=-1
            for i in range(len(SensorBelt)):
                if(self.getDistanceAtSensor(i)<1):
                    if(i==0 or i==7):
                        translation=1
                    if(i>0 and i<=3):
                        rotation+=1
                    if(i>3 and i<7):
                        rotation-=1
            if(rotation>1):
                rotation=1
            if(rotation<-1):
                rotation=-1
            if(rotation==0):
                rotation=-1
            self.setTranslationValue(translation)
            self.setRotationValue(rotation)
            continuous_state=15
            
        else:
            (translation,rotation) = maSub1.actionChoisie(self)
            self.setTranslationValue(translation)
            self.setRotationValue(rotation)
            
    		# monitoring (optionnel - changer la valeur de verbose)
            if verbose == True:
    	        print "Robot #"+str(self.id)+" [teamname:\""+str(self.teamname)+"\"] [variable mémoire = "+str(self.etat)+"] :"
    	        for i in range(len(SensorBelt)):
    	            print "\tSenseur #"+str(i)+" (angle: "+ str(SensorBelt[i])+"°)"
    	            print "\t\tDistance  :",self.getDistanceAtSensor(i)
    	            print "\t\tType      :",self.getObjectTypeAtSensor(i) # 0: rien, 1: mur ou bord, 2: robot
    	            print "\t\tRobot info:",self.getRobotInfoAtSensor(i) # dict("id","centroid(x,y)","orientation") (si pas de robot: renvoi "None" et affiche un avertissement dans la console
        new_x=int(self.getRobot().get_centroid()[0])
        new_y=int(self.getRobot().get_centroid()[1])
        has_moved=(x_state-new_x!=0 or y_state-new_y!=0)
        if(has_moved):
            new_m=(m_state%2)*2+(1)
        else:
            new_m=new_m=(m_state%2)*2+(0)
        self.etat=continuous_state*pow(2,22)+new_m*pow(2,20)+new_x*pow(2,10)+new_y

        # ^^^^^^^^^^^^^
        #
        #
        #
        #

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
        if invertInitPop == True:
            agents.append(AgentTypeB(p))
        else:
            agents.append(AgentTypeA(p))

    for i in range(nbAgentsTypeB):
        p = game.add_players( (486 , 200+32*i) , None , tiled=False)
        p.oriente( 180 )
        p.numero = nbAgentsCreated
        nbAgentsCreated = nbAgentsCreated + 1
        if invertInitPop == True:
            agents.append(AgentTypeA(p))
        else:
            agents.append(AgentTypeB(p))

    game.mainiteration()



def setupArena0(): # classic
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

def setupArena1(): # the void
    return

def setupArena2(): # the gaps
    for i in range(0,3):
        addObstacle(row=i,col=7)
    for i in range(4,13):
        addObstacle(row=i,col=7)
    for i in range(14,16):
        addObstacle(row=i,col=7)

def setupArena3(): # the cross
    for i in range(3,12):
        if i != 7:
            addObstacle(row=i,col=6)
            addObstacle(row=i,col=8)
    for j in range(3,12):
        if not(j >= 6 and j <= 7):
            addObstacle(row=6,col=j)
            addObstacle(row=8,col=j)

def setupArena4(): # the lanes
    for i in range(0,15):
        for j in range(2,7,2):
            addObstacle(row=(j/2)%2+i,col=j)
    for i in range(0,15):
        for j in range(9,15,2):
            addObstacle(row=(j/2)%2+i,col=j)
    return

'''
def setupArena5(): # the vault
    for i in range(0,5):
        addObstacle(row=11,col=i)
        addObstacle(row=4,col=i)
        addObstacle(row=11,col=11+i)
        addObstacle(row=4,col=11+i)
    for i in range(1,3):
        addObstacle(row=11-i,col=11)
        addObstacle(row=4+i,col=4)
    addObstacle(row=5,col=11)
    addObstacle(row=10,col=4)
    return
'''

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
    if running == True:
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

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 1:
    arena = int(sys.argv[1])
    print "Arena: ", str(arena), "(user-selected)"
    if len(sys.argv) == 3:
        if sys.argv[2] == "True" or sys.argv[2] == "true":
            invertInitPop = True
        if invertInitPop == False:
            print "Equipe BLEUE commence à gauche."
        else:
            print "Equipe VERTE commence à gauche."
else:
    print "Arena: ", str(arena), "(default), équipe BLEUE commence à gauche."

if arena == 0:
    setupArena0()
elif arena == 1:
    setupArena1()
elif arena == 2:
    setupArena2()
elif arena == 3:
    setupArena3()
elif arena == 4:
    setupArena4()
else:
    print "labyrinthe inconnu."
    exit (-1)

running = True

setupAgents()
game.mainiteration()

iteration = 0
while iteration != maxIterations:
    stepWorld()
    game.mainiteration()
    if iteration % 200 == 0:
        displayOccupancyGrid()
    iteration = iteration + 1

