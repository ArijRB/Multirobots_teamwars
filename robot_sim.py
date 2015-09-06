from gameclass import Game
from sprite import MySprite,MovingSprite
from players import Player,Turtle
from spritebuilder import SpriteBuilder
import random
from math import pi,cos,sin

class TurtleSpriteBuilder(SpriteBuilder):
    def basicSpriteFactory(self,spritegroups , layername,tileid,x,y,img):
        if layername == "joueur":
            j = Turtle(layername,tileid,x,y,[img])
            spritegroups[layername].add( j )
            j.build_fleche()
        else:
            SpriteBuilder.basicSpriteFactory(spritegroups,layername,tileid,x,y,img)

###########################################

game = Game('Cartes/robot_obstacles.json',TurtleSpriteBuilder)
game.mainiteration()

def avance(s):
    global game
    game.player.forward(s)
    game.mainiteration()
    return game.player.position_changed()

def setheading(a):
    # angle en degre
    global game
    game.player.translate_sprite(0,0,a)
    #game.player.rotate(a,False)
    game.mainiteration()

def telemetre():
    global game
    rayon_hit = game.player.throw_ray(game.player.angle_degree*pi/180 , game.mask,game.groupDict)
    game.mainiteration()
    return game.player.dist(*rayon_hit)
