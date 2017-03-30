#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robosim import *
from random import random, shuffle
import time
import sys
import atexit

from teamwars_parameters import *


class AgentTypeA(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    teamname = "A"
    robotname = ""
    
    def __init__(self,robot):
        self.id = AgentTypeA.agentIdCounter
        AgentTypeA.agentIdCounter = AgentTypeA.agentIdCounter + 1
        self.name = str(self.teamname)+str(self.id)
        self.robot = robot
    
    def getTeamname(self):
        return self.teamname
    
    def getRobotname(self):
        return self.robotname
    
    def getRobot(self):
        return self.robot
    
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR A -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    teamname = "Equipe Alpha" # A modifier avec le nom de votre équipe
    
    def step(self,sensors):
        
        color( (0,255,0) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot
        
        #print "robot #", self.id, " -- step"
        
        p = self.robot
        
        # actions
        sensor_infos = sensors[p] # sensor_infos est une liste de namedtuple (un par capteur).
        #print "sensor_infos: ", sensor_infos[0].dist_from_border
        distGauche = sensor_infos[2].dist_from_border
        if distGauche > maxSensorDistance:
            distGauche = maxSensorDistance # borne
        distDroite = sensor_infos[5].dist_from_border
        if distDroite > maxSensorDistance:
            distDroite = maxSensorDistance # borne
        
        if distGauche < distDroite:
            self.setRotationValue( +1 )
        elif distGauche > distDroite:
            self.setRotationValue( -1 )
        else:
            self.setRotationValue( 0 )
        
        self.setTranslationValue(1) # normalisé -1,+1
        
        # self.displayInfo(sensors)
        
        return
    
    
    def displayInfo(self,sensors):
        
        p = self.robot
        

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
                        print "  - type: robot no." + str(playerTMP.numero) + " with name "
                        print "    - x,y = " + str( playerTMP.get_centroid() ) + ")" # renvoi un tuple
                        print "    - orientation = " + str( playerTMP.orientation() ) + ")" # p/r au "nord"
                    elif impact.layer == 'obstacle':
                        print "  - type obstacle"
                    else:
                        print "  - type boundary of window"
        return

    
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    def setTranslationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxTranslationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxTranslationSpeed
        else:
            value = value * maxTranslationSpeed
        self.robot.forward(value)
    
    def setRotationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxRotationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxRotationSpeed
        else:
            value = value * maxRotationSpeed
        self.robot.rotate(value)
    
    def getDistanceFromSensor(self, index):
        return max(sensor_infos[2].dist_from_border,maxSensorDistance)
    
    def getTeamnameFromRobot(self,agent):
        return agents[agent.sprite.numero].teamname
