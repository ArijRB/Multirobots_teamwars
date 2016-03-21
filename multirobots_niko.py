# coding: utf-8

from robosim import *
from random import random
import time




def addObstacle(row,col):
    # le sprite situe colone 13, ligne 0 sur le spritesheet
    game.add_new_sprite('obstacle',tileid=(0,13),xy=(col,row),tiled=True)



"""
    Si tu veux limiter la vitesse des robots, alors le plus simple est de deriver la classe Turtle
"""
class MyTurtle(Turtle):
    maxRotationSpeed = 10000 #unlimited
    def rotate(self,a):
        mx = MyTurtle.maxRotationSpeed
        Turtle.rotate(self, max(-mx,min(a,mx)))

###########################################



'''
Note que ci-dessous, je redimensionne la fenetre comme je le souhaite
et je donne la nouvelle classe MyTurtle a init pour qu'il sache comment creer des
nouveaux players
'''

game = Game()
init('vide2',MyTurtle,screen_width=768,screen_height=768)

'''
le auto_refresh=False signifie que l'ecran ne sera remis a jour
que lors des appels explicites a game.mainiteration()
'''
game.auto_refresh = False




# Arene
for i in range(10,14):
    addObstacle(row=2,col=i)

print "Arene: " + str(taille_terrain()) # donne width height de l'arene

# Initialisation robots
maxSensorDistance = 200              # utilisé localement.

MyTurtle.MaxRotationSpeed = 10 # donc entre -10 et 10
#game.setMaxTranslationSpeed(3) # donc entre -3 et 3

SensorBelt = [-80,-40,0,40,80]  # angles en degres

# Make 30 agents
for i in range(50):
    while True:
        p = -1
        while p == -1: # p renvoi -1 s'il n'est pas possible de placer le robot ici (obstacle)
            p = game.add_players( (random()*500 , random()*500) , game.player , tiled=False)
        if p:
            p.rotate( random()*360 )
            break

game.mainiteration()


for i in range(1000):

    # c'est plus rapide d'appeler cette fonction une fois pour toute car elle doit recalculer le masque de collision,
    # ce qui est lourd....
    sensors = throw_rays_for_many_players(game,game.layers['joueur'],SensorBelt,show_rays=True)

    for p in game.layers['joueur']:

        p.rotate( random()*3 )   # normalisé -1,+1 -- valeur effective calculé avec maxRotationSpeed et maxTranslationSpeed
        p.forward(1) # normalisé -1,+1

        # pour ne pas surcharger l'affichage, je ne fais ca que pour le player 1
        if p == game.player:

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

    game.mainiteration()
