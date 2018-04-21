#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 21:45:31 2018

@author: arij
"""

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