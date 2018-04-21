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
invertInitPop = True

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

    teamname = "Equipe BLEUE" # A modifier avec le nom de votre équipe

    def stepController(self):
        
        color( (0,0,255) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot

        def bitfield(n):#Convertit un entier en un tableau de bits de longueur 32
            a = [1 if digit=='1' else 0 for digit in bin(n)[2:]]
            if(len(a) != 32):
                b = [0]*(32-len(a))
            return b+a
    
        def bitlisttoint(l):#Convertit une liste de bits en entier
            tot = 0
            for i in range(0,len(l)):
                tot+=l[i]*(2**(len(l)-1-i))
            return tot
            
        def inttobitlist(x,length):#Convertit un entier en une liste de bits
            tab  = []
            for i in range(0,length):
                    if x >= 2**(length -i-1):
                            x = x- 2**(length -i-1)
                            tab.append(1)
                    else:
                            tab.append(0)
            return tab
                
        def setEtat(posX,posY,nbStuck,deblock,ori,depl,autoRot):#Initialise la variable etat
            tab = []
            tab +=inttobitlist(int(posX), 6)
            tab +=inttobitlist(int(posY), 6)
            tab += inttobitlist(nbStuck,5)
            tab.append(deblock)
            tab +=inttobitlist(ori,9)
            tab +=inttobitlist(depl,2)
            tab.append(autoRot)
            tab.append(0)
            tab.append(0)
            self.etat=bitlisttoint(tab)
            return self.etat
    
        def getEtat():#Récupère les différentes variables stockées dans etat
            l = bitfield(self.etat)
            posX = bitlisttoint(l[0:6])
            posY = bitlisttoint(l[6:12])
            nbStuck = bitlisttoint(l[12:17])
            deblock = bitlisttoint(l[17:18])
            ori = bitlisttoint(l[18:27])
            depl = bitlisttoint(l[27:29])
            autoRot = bitlisttoint(l[29:30])
            if(verbose):
                print("Etat")
                print(posX)
                print(posY)
                print(nbStuck)
                print(deblock)
                print(ori)
                print(depl)
                print(autoRot)
            return posX,posY,nbStuck,deblock,ori,depl,autoRot
        
        def step():
            self.stepController()
    
        def move():#Effectue les mouvements determinées par le stepController
            self.robot.forward(self.translationValue)
            if verbose:
                print("Rotate")
                print(self.rotationValue)
            self.robot.rotate(self.rotationValue)
        
        def suite(bg,ahg,fhg,fhd,ahd,bd):#En fonction des capteurs activés, determine un coté du robot sans obstacle
            tab = [bg,ahg,fhg,fhd,ahd,bd]
            lenmaxSuite = -1
            iminsuite = -1
            imaxsuite = -1
            imin = -1
            imax = -1
            lenActu = 0
            for i in range(len(tab)):
                if(tab[i] == 0):
                    imin = i
                    lenActu = 0
                    for j in range(len(tab)):
                        if(tab[(i+j)%6] == 0):
                            imax = (i+j)
                            lenActu+=1
                        else:
                            break
                    if(lenActu > lenmaxSuite):
                        lenmaxSuite = lenActu
                        iminsuite = imin
                        imaxsuite = imax
            iret = int((imaxsuite+iminsuite)/2)%6
            return SensorBelt[iret]
        
        def stuck(trigSens):#Si la position du robot reste la même pendant un moment il faut le debloquer
            x,y = self.robot.get_centroid()
            rot = 0.
            posX,posY,nbStuck,deblocage,ori,depl,autoRot = getEtat()
            depl = -1
            if(deblocage == 0):
                if(int(x/16) == posX and int(y/16) == posY):
                    nbStuck += 1
                    if(nbStuck == 32):
                        ori = 0
                        depl = 0
                        deblocage = 1
                        ts = [i for i in range(len(trigSens)) if trigSens[i]==True]
                        g = 0
                        d = 0
                        bg = 0
                        bd = 0
                        ahd = 0
                        ahg = 0
                        fhd = 0
                        fhg = 0
                        for i in ts:
                            if(i <= 3 and i >= 1):
                                g=1
                            elif(i <= 6 and i >= 4):
                                d=1
                            elif(i == 0):
                                bg =1
                            elif(i == 7):
                                bd =1
                            if(i == 2 or i == 3):
                                fhg=1
                            elif(i == 4 or i == 5):
                                fhd=1
                            elif(i == 1):
                                ahg =1
                            elif(i == 6):
                                ahd =1
                        ori =  self.robot.orientation() + suite(bg,ahg,fhg,fhd,ahd,bd)
                        depl = 1
                else:
                    posX = int(x/16)
                    posY = int(y/16)
                    nbStuck = 0
            else:
                if(ori == self.robot.orientation() or(abs(ori-self.robot.orientation()) < maxRotationSpeed or abs(ori - self.robot.orientation()) > (360 - maxRotationSpeed))):
                    deblocage = 0
                    nbStuck = 0
                else:
                    rot = ori-self.robot.orientation()
                    if( abs(rot) < maxRotationSpeed and abs(rot) > 1):
                        rot = rot/maxRotationSpeed
            setEtat(posX,posY,nbStuck,deblocage,ori,depl,autoRot)
            if(deblocage==1):
                return rot , depl,True
            else:
                return 0.,0.,False
         
        def avoidObstacle(trigSens, tsc,dist):#Arbre de comportement determinant l'orientation a avoir pour eviter des obstacles
            ts = [i for i in range(len(trigSens)) if trigSens[i]==True]
            gCount = 0
            dCount = 0
            bg = 0
            bd = 0
            ahd = 0
            ahg = 0
            fhd = 0
            fhg = 0
            for i in ts:
                if(i <= 3 and i >= 1):
                    gCount+=1
                elif(i <= 6 and i >= 4):
                    dCount+=1
                elif(i == 0):
                    bg +=1
                elif(i == 7):
                    bd +=1
                if(i == 2 or i == 3):
                    fhg+=1
                elif(i == 4 or i == 5):
                    fhd+=1
                elif(i == 1):
                    ahg +=1
                elif(i == 6):
                    ahd +=1
            if(ts == 0):
                return 1,0,False #Forward
            elif(tsc ==1):
                if(ts[0]<=1 or ts[0]>=6):
                    return 1,0, False#Forward
                elif(fhd):
                        return 1,SensorBelt[1], True#GO AHG
                elif(fhg):
                        return 1,SensorBelt[5], True#go ahd
                elif(ahg):
                        return 1 , SensorBelt[4], True#Go fhd 4
                elif(ahd):
                        return 1,SensorBelt[3], True#Go fhg 3
                else:
                    return 0,-SensorBelt[ts[0]], True #Rotate angle sensor triggered
            elif(tsc == 2):
                if((ts[0],ts[1]) == (0,1) or (ts[0],ts[1]) == (0,7) or (ts[0],ts[1]) == (0,6)):
                    return 1,0, False#Forward!
                elif(ts[0] <= 3 and ts[0] >= 1 and ts[1] <= 6 and ts[1] >= 4):
                    if(dist[ts[0]] < dist[ts[1]]):
                        return 1,SensorBelt[ts[1]], True
                    else:
                        return 1,SensorBelt[ts[1]], True
                else:
                    if(fhd and bd):#4 6
                        return 1,SensorBelt[1], True#GO AHG
                    elif(fhd and bg):#4 1
                        return 1,SensorBelt[2], True#Go fhg 2
                    elif(fhd and ahd): # 4 5 
                        return 1,SensorBelt[1], True#Go ahg
                    elif(fhd and ahg): # 4 2
                        return 1,SensorBelt[6], True#Go bd
                    elif(fhd and fhg): # 4 3
                        return 1,180, True#Demi Tour
                    elif(fhg and bd):# 3 6
                        return 1,SensorBelt[5], True#Go fhg 5
                    elif(fhg and bg):#3 1
                        return 1,SensorBelt[5], True#go ahd
                    elif(fhg and ahd): # 3 5 
                        return 1,SensorBelt[1], True#Go bg
                    elif(fhg and ahg): # 3 2
                        return 1,SensorBelt[5], True#Go ahd
                    elif(ahg and bg):#1 2
                        return 1 , SensorBelt[4], True#Go fhd 4
                    elif(bg and bg):#1 6
                        return 1 , 0, True#Go fhg 2
                    elif(fhg == 2): # 3 3 
                        return 1, SensorBelt[5], True #Go FHD 5
                    elif(fhd == 2): # 4 4
                        return 1, SensorBelt[2], True #Go FHG 2
                    else:
                        return 1 , 0, True#Forward!
                        
                    
            elif(tsc == 3):
                if(ts[0] in [0,1,6,7] and ts[1] in [0,1,6,7] and ts[2] in [0,1,6,7]):
                    return 1,0,False#Forward
                else:
                    
                        
                    if(gCount == 3 or dCount == 3):
                        if(dist[ts[0]] > dist[ts[1]] and dist[ts[0]] > dist[ts[2]]):
                            return 1,-SensorBelt[ts[0]], True
                        elif(dist[ts[1]] > dist[ts[0]] and dist[ts[1]] > dist[ts[2]]):
                            return 1,-SensorBelt[ts[1]], True
                        elif(dist[ts[2]] > dist[ts[1]] and dist[ts[2]] > dist[ts[0]]):
                            return 1,-SensorBelt[ts[2]], True
                    elif(bg == 1):
                        if(gCount != 0 and dCount == 0):
                            return 1,SensorBelt[5], True#Direction HD
                        elif(gCount == 0 and dCount != 0):
                            return 1,SensorBelt[2], True#Direction HG
                        else:
                            return 1,SensorBelt[7], True#Direction BD
                    elif(bd == 1):#Detection bas droite
                        if(dCount != 0 and gCount == 0):
                            return 1,SensorBelt[2], True#Direction HG
                        elif(dCount == 0 and gCount != 0):
                            return 1,SensorBelt[5], True#Direction HD
                        else:
                            return 1,SensorBelt[0], True#Direction BG
                    elif(gCount+dCount == 3): #Si on est coincé entre deux mur devant nous, on cherche une orientation parmis [1 (2,3) (4,5) 6]
                        if(fhg != 0 and fhd != 0 and fhg + fhd == 3):
                            if(fhg < fhd):
                                return 1 , SensorBelt[1], True#Go ahg
                            else:
                                return 1, SensorBelt[5], True
                        elif(fhg == 0):
                            return 1,SensorBelt[2], True
                        elif(fhd == 0):
                            return 1,SensorBelt[4], True
                        elif(ahg == 0):
                            return 1,SensorBelt[1], True
                        elif(ahd == 0):
                            return 1,SensorBelt[6], True
                        elif(dist[ts[0]] > dist[ts[1]] and dist[ts[0]] > dist[ts[2]]):
                            return 1,SensorBelt[ts[0]], True
                        elif(dist[ts[1]] > dist[ts[0]] and dist[ts[1]] > dist[ts[2]]):
                            return 1,SensorBelt[ts[1]], True
                        elif(dist[ts[2]] > dist[ts[1]] and dist[ts[2]] > dist[ts[0]]):
                            return 1,SensorBelt[ts[2]], True
                if(6 in ts) :
                    return  0,SensorBelt[1],True
                elif(1 in ts) :
                    return  0,SensorBelt[6],True
                else:
                    return 0, -SensorBelt[ts[0]],True
                    
            elif(tsc == 4):
                if(ts == [2,3,4,5]):
                    return 0, 90, True
                elif(ts == [3,4,5,6]):
                    return 0, -90, True
                elif(ts == [1,2,3,4]):
                    return 0, 90, True
                else:
                    return  0,0,False
            elif(tsc == 5):
                if(set([2,3,4,5]).issubset(set(ts))):
                    if(1 in ts or 0 in ts):
                        return 0, 90, True
                    elif(6 in ts or 7 in ts):
                        return 0, -90, True
                else:
                    return 0,0,False
            elif(tsc == 6):
                if(0 not in ts and 7 not in ts):
                    return 0,180,True
                for k in range(0,8):
                    if(k not in ts):
                        return 0,SensorBelt[k],True
                return 0,0,False
            else:
                return  0,0,False
    
        def closeToWall(trigWall,tsc, dist):#Si un robot est proche d'un mur, il essaiera de se mettre parallèle a lui pour le longer
            ts = [i for i in range(len(trigWall)) if trigWall[i]==True and dist[i] < 0.3]    
            gCount = 0
            dCount = 0
            bg = 0
            bd = 0
            ahd = 0
            ahg = 0
            fhd = 0
            fhg = 0
            for i in ts:
                if(i <= 3 and i >= 1):
                    gCount+=1
                elif(i <= 6 and i >= 4):
                    dCount+=1
                elif(i == 0):
                    bg +=1
                elif(i == 7):
                    bd +=1
                if(i == 2 or i == 3):
                    fhg+=1
                elif(i == 4 or i == 5):
                    fhd+=1
                elif(i == 1):
                    ahg +=1
                elif(i == 6):
                    ahd +=1
            if((ahg != 0 or ahd != 0) and (fhd+fhg == 0)):
                return 1,0,True
            if(fhd != 0 and fhg != 0):
                if(ahd == 0):
                    if(5 in ts):
                        return 1,SensorBelt[5]-SensorBelt[1],True
                    elif(4 in ts):
                        return 1,SensorBelt[4]-SensorBelt[1],True
                elif(ahg == 0):
                    if(2 in ts):
                        return 1,SensorBelt[2]-SensorBelt[6],True
                    elif(3 in ts):
                        return 1,SensorBelt[3]-SensorBelt[6],True
                else:
                    return -1, 180*(int(random())*2-1),True
            if(fhd != 0):
                if(4 in ts):
                    return 1,SensorBelt[4]-SensorBelt[6],True
                elif(5 in ts):
                    return 1,SensorBelt[5]-SensorBelt[6],True
            if(fhg != 0):
                if(3 in ts):
                    return 1,SensorBelt[3]-SensorBelt[1],True
                elif(2 in ts):
                    return 1,SensorBelt[2]-SensorBelt[1],True
            if(bg != 0):
                if(ahg == 0):
                    return 1,SensorBelt[0]-SensorBelt[1],True
                    
                elif(ahg == 0):
                    return 1,SensorBelt[0]-SensorBelt[6],True
            if(bd != 0):
                if(ahg == 0):
                    return 1,SensorBelt[7]-SensorBelt[1],True
                    
                elif(ahg == 0):
                    return 1,SensorBelt[7]-SensorBelt[6],True
                    
            return 0,0,False
                                    
        def partAway(tsr,irh):#Si on detecte un allié près de nous on essaie de s'en eloigner
            ts = [i for i in range(len(tsr)) if tsr[i]==True]
            if(len(ts) != 0):
                for i in ts:
                    if(irh[i]["teamname"] == self.robot.teamname):
                        return 1, -SensorBelt[i], True
            return 0,0,False
              
        def followAFoe(tsr,irh):#Si opn detecte un adversaire, on cherche a le suivre
            ts = [i for i in range(len(tsr)) if tsr[i]==True]
            for i in ts:
                if(irh[i]["teamname"] == self.robot.teamname):
                    return 0,0,False
            if(len(ts )!= 0):
                for i in ts:
                    if(irh[i]["teamname"] != self.robot.teamname):
                        return 1,SensorBelt[i],True
            return 0,0,False
                    
    
        def archSubsomption(dist,trigSens,tsc,tsw,tsr,irh):#Architecture de subsomption gerant les déplacements du robot
            p = self.robot
            directionDefault = 1
            rotationDefault = 0
            d2,r2,b2 = avoidObstacle(trigSens,tsc,dist)
            d,r,b= stuck(trigSens)
            d5,r5,b5 = closeToWall(tsw,tsc,dist)
            d3,r3,b3 = followAFoe(tsr,irh)
            d4,r4,b4 = partAway(tsr,irh)
            
            if(b):#Si le robot est bloqué on utilise la fonction de debloquage
                self.setRotationValue(r)
                self.setTranslationValue(d)
            elif(b3):#Si on detecte un robot adverse on cherche a le suivre (jusqu'a ce qu'il s'immobilise ou qu'on le perde)
                self.setRotationValue(r3)
                self.setTranslationValue(d3)
            elif(b2):#On evite les murs
                self.setRotationValue(r2)
                self.setTranslationValue(d2)
            elif(b4):#On s'écarte des alliés
                self.setRotationValue(r4)
                self.setTranslationValue(d4)
            else:#Biais avance et tourne legerement a gauche ou droite (a chaque tour, 10% de chance de changer de "direction"
                self.setTranslationValue(directionDefault)
                if(tsc == 0):
                    posX,posY,nbStuck,deblock,ori,depl,autoRot = getEtat()
                    if(autoRot == 0):
                        self.setRotationValue(0.1)#6 Déterminé par recherche
                    if(autoRot == 1):
                        self.setRotationValue(-0.1)
                    if(int(random()*100)> 90):
                        autoRot = (autoRot+1)%2
                    setEtat(posX,posY,nbStuck,deblock,ori,depl,autoRot)
        
        triggeredSensorsCount = 0
        triggeredSensors = [False]*8
        triggeredSensorsWall = [False]*8
        triggeredSensorsRobot = [False]*8
        infoRobotHit = [None]*8
        #triggeredSensors = [False,False,False,False,False,False,False,False]
        triggeredSensorsDist = [10000.0]*8
        # monitoring - affiche diverses informations sur l'agent et ce qu'il voit.
        # pour ne pas surcharger l'affichage, je ne fais ca que pour le player 1
        for i in range(len(SensorBelt)):
            if(self.getDistanceAtSensor(i) < (maxSensorDistance)):#2.4 trouvé par recherche aléatoire
                if(self.getObjectTypeAtSensor(i) != 0):
                    triggeredSensorsDist[i] = self.getDistanceAtSensor(i)
                    triggeredSensors[i] = True
                    triggeredSensorsCount+=1
                    if(self.getObjectTypeAtSensor(i) == 1):
                        triggeredSensorsWall[i] = True
                    elif(self.getObjectTypeAtSensor(i) == 2):
                        triggeredSensorsRobot[i] = True
                        infoRobotHit[i] = self.getRobotInfoAtSensor(i)
                    
                if verbose == True:
                    print( "\tSenseur #"+str(i)+" (angle: "+ str(SensorBelt[i])+"°)")
                    print( "\t\tDistance  :",self.getDistanceAtSensor(i))
                    print( "\t\tType      :",self.getObjectTypeAtSensor(i))# 0: rien, 1: mur ou bord, 2: robot
                    print( "\t\tRobot info:",self.getRobotInfoAtSensor(i)) # dict("id","centroid(x,y)","orientation") (si pas de robot: renvoi "None" et affiche un avertissement dans la console

        

        archSubsomption(triggeredSensorsDist,triggeredSensors,triggeredSensorsCount,triggeredSensorsWall,triggeredSensorsRobot,infoRobotHit)





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

